from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func,CharField
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

from committees.models import Position
from borrowers.models import Borrower
from loans.models import CreditLine,Loan,Amortization,AmortizationItem
from documents.models import Document
from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from loans.models import Status,AmortizationStatus,LoanStatus,Loan
from django.utils import timezone
from loans import PMT

from datetime import datetime
from decimal import Decimal
from users.models import CustomUser


def excludeWeekends(amortizationItems):

    for amortizationItem in amortizationItems.all():

        weekno= amortizationItem.schedule.weekday()
     
        if weekno == 5:
            amortizationItem.schedule = amortizationItem.schedule + timezone.timedelta(days=2)
        if weekno == 6:
            amortizationItem.schedule = amortizationItem.schedule + timezone.timedelta(days=1) 

        amortizationItem.save()
def generateAmortizationSchedule(loan,request):
    
    noOfPrincipalPaymentSchedules = loan.term.days / loan.term.principalPaymentPeriod.paymentCycle
    # noOfPaymentSchedules = loan.term.days / loan.term.paymentPeriod.paymentCycle
    noOfInterestPaymentSchedules = loan.term.days / loan.term.interestPaymentPeriod.paymentCycle

    if noOfPrincipalPaymentSchedules > noOfInterestPaymentSchedules:
     
        noOfPaymentSchedules = noOfPrincipalPaymentSchedules

    else:
        noOfPaymentSchedules = noOfInterestPaymentSchedules

    cycle = loan.term.interestPaymentPeriod.paymentCycle

    schedule = loan.dateReleased  + timezone.timedelta(days=cycle)

    pmt = PMT()
    pmtInterest = PMT()
    print(pmt.payment)
    print(pmt.nextStartingValue)
    print(pmt.interest)
    print(pmt.principal)

    loanAmount = loan.amount

    amortization = Amortization( 
            loan = loan,
            dateReleased = loan.dateReleased  ,
            # dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
            amortizationStatus = AmortizationStatus.objects.get(pk=1),
            createdBy = request.user,
            schedules = noOfPaymentSchedules,
            cycle = cycle,
            termDays = loan.term.days
        )
    amortization.save()
    currentCycle = 1
    interestLoan = loan.amount
    for i in range(int(noOfPaymentSchedules)):

        pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
        lastPayment = schedule  
        dayTillCutOff = cycle - int(lastPayment.strftime ('%d') )

        print("interest rate")
       
        print(Decimal((pmt.principal + pmt.nextStartingValue) - pmt.interest))
        accruedInterest = Decimal((pmt.principal + pmt.nextStartingValue) ) * (loan.interestRate.interestRate/100) *  dayTillCutOff/360
        print(round(accruedInterest,2))
        
        amortizationItem = AmortizationItem(
            schedule = schedule,
            amortization = amortization,
            days= cycle,
            principal = pmt.principal,
            deductAccruedInterest =  pmt.interest- accruedInterest,
            accruedInterest = accruedInterest,
            interest = pmt.interest,
            additionalInterest = 0,
            penalty = 0,
            vat = 0,
            total = pmt.payment,
            principalBalance = pmt.nextStartingValue,
            amortizationStatus = AmortizationStatus.objects.get(pk=1), 
        )
        amortizationItem.save()

        schedule = schedule + timezone.timedelta(days=cycle)
        loanAmount = pmt.nextStartingValue

         
    # excludeWeekends(amortization.amortizationItems) 
def generateUnevenAmortizationSchedule(loan,request):

 
    noOfPrincipalPaymentSchedules = loan.term.days / loan.term.principalPaymentPeriod.paymentCycle
    # noOfPaymentSchedules = loan.term.days / loan.term.paymentPeriod.paymentCycle
    noOfInterestPaymentSchedules = loan.term.days / loan.term.interestPaymentPeriod.paymentCycle

    if noOfPrincipalPaymentSchedules > noOfInterestPaymentSchedules:
     
        noOfPaymentSchedules = noOfPrincipalPaymentSchedules

    else:
        noOfPaymentSchedules = noOfInterestPaymentSchedules

    cycle = loan.term.interestPaymentPeriod.paymentCycle

    schedule = loan.dateReleased  + timezone.timedelta(days=cycle)

    pmt = PMT()
    pmtInterest = PMT()
    print(pmt.payment)
    print(pmt.nextStartingValue)
    print(pmt.interest)
    print(pmt.principal)

    loanAmount = loan.amount

    amortization = Amortization( 
            loan = loan,
            dateReleased = loan.dateReleased  ,
            # dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
            amortizationStatus = AmortizationStatus.objects.get(pk=1),
            createdBy = request.user,
            schedules = noOfPaymentSchedules,
            cycle = cycle,
            termDays = loan.term.days
        )
    amortization.save()
    currentCycle = 1
    interestLoan = loan.amount
    for i in range(int(noOfPaymentSchedules)):

        pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
        principaEntry = 0
        pmtInterest = pmtInterest.getPayment(interestLoan,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
        if (cycle  *  (i+1)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle) : 
        # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):
            
            # pmtPrincipal = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPrincipalPaymentSchedules,noOfPrincipalPaymentSchedules - i)

            principaEntry = int(loan.amount) / noOfPrincipalPaymentSchedules
        print(i)
        lastPayment = schedule - timezone.timedelta(days=cycle)
      
        dayTillCutOff = cycle - int(lastPayment.strftime ('%d') ) 
       
        accruedInterest = (int(pmt.principal)) * (loan.interestRate.interestRate/100) *  dayTillCutOff/360
        amortizationItem = AmortizationItem(
            schedule = schedule,
            amortization = amortization,
            days= cycle,
            principal = principaEntry,
            deductAccruedInterest =  pmtInterest.interest- accruedInterest,
            accruedInterest = accruedInterest,
            interest = pmtInterest.interest,
            additionalInterest = 0,
            penalty = 0,
            vat = 0,
            total = int(principaEntry) + pmtInterest.interest,
            principalBalance = pmt.nextStartingValue,
            amortizationStatus = AmortizationStatus.objects.get(pk=1), 
        )
        amortizationItem.save()

        schedule = schedule + timezone.timedelta(days=cycle)
        loanAmount = pmt.nextStartingValue

        if (cycle  *  (i+1)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle) : 
        # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):
            # loanAmount = pmt.nextStartingValue
            
            currentCycle  = currentCycle + 1
            interestLoan = int(principaEntry)
    # excludeWeekends(amortization.amortizationItems) 

class CreditLineApprovedView(views.APIView):
    
    # @method_decorator(csrf_protect)
    def post(self,request):

        documentid = request.data.get("documentid") 
        if documentid:  
            document = Document.objects.get(pk=documentid)
            document.dateApproved = timezone.now()
            document.save()

            creditLine = document.creditLine
            creditLine.dateApproved = timezone.now()
            creditLine.dateExpired = timezone.now() + timezone.timedelta(days=365)


            creditLine.status= Status.objects.get(pk=6) #APPROVED
            creditLine.save()


            return Response({
                'status': 'Accepted',
                'message': 'Credit Line Updated'
            },status= status.HTTP_202_ACCEPTED)
 
        return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)

class LoanAvailmemtApprovedView(views.APIView):
    
    # @method_decorator(csrf_protect)
    def post(self,request):

        documentid = request.data.get("documentid") 
        print(documentid)
        if documentid:  
            document = Document.objects.get(pk=documentid)
            document.dateApproved = timezone.now()
            document.save()

            loan = document.loan
            loan.dateApproved = timezone.now() 

            loan.loanStatus= LoanStatus.objects.get(pk=1) #APPROVED
            loan.save()
    

            return Response({
                'status': 'Accepted',
                'message': 'Loan Updated'
            },status= status.HTTP_202_ACCEPTED)
 
        return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)

 
class SaveDraftRestructuredAmortizationView(views.APIView):

    def post(self,request):

        params = request.data.get("params") 
        amortizationId = params["amortizationId"]

        loanId = params["loanId"]


        # amortization = Amortization.objects.filter(loan__id=loanId,amortizationStatus__id=1).first()
        # if amortization:
        #     amortization.amortizationStatus = AmortizationStatus.objects.get(pk=5) #VOID
        #     amortization.save()
        # else: 
        #     return Response({'error':'Error on Saving Draft'},status.HTTP_400_BAD_REQUEST)
        
        amortization = Amortization.objects.filter(loan__id=loanId,amortizationStatus__id=1).first() #PAID

        if amortization:
            amortization.amortizationStatus = AmortizationStatus.objects.get(pk=6) #RESTRUCTURED
            amortization.save()
        # else: 
        #     return Response({'error':'Error on Saving Draft'},status.HTTP_400_BAD_REQUEST)

        amortization = Amortization.objects.get(id=amortizationId)
        loan = Loan.objects.get(pk=loanId)
        loan.loanStatus = LoanStatus.objects.get(id=10) #RESTRUCTURED
        loan.isRestructured = True
        loan.save()

        
        loan.isRestructured = False

        loan.latestPayment = loan.getLatestPayment()
        print("current")
        if loan.latestPayment:
            loan.amount = loan.latestPayment.principalBalance
            print("latestPayment")
            print(loan.latestPayment.principalBalance)

        print(loan.amount)
        loan.pk=None
        loan.loanStatus = LoanStatus.objects.get(id=3) #RESTRUCTURED CURRENT
        loan.save()

       
        if amortization:
            amortization.amortizationStatus = AmortizationStatus.objects.get(pk=1) #UNPAID
            amortization.loan = loan
            amortization.save()
        else: 
            return Response({'error':'Error on Saving Draft'},status.HTTP_400_BAD_REQUEST)

         


        return Response({
            'success':'true',
            'message': 'Restructured Amortization Generated',
            'loanId':loan.id

        },status= status.HTTP_202_ACCEPTED)


class CalculateRestructurePMTView(views.APIView):
    
    # @method_decorator(csrf_protect) 

    def post(self,request):
        params = request.data.get("params") 
        
        print(params)
         
        dateStart = datetime.strptime(params["dateStart"], '%m/%d/%Y')  
         
        principalPaymentCycle = params["principalPaymentCycle"]
        interestPaymentCycle = params["interestPaymentCycle"]
        
        termDays = params["termDays"]
        loanId = params["loanId"]

        loan = Loan.objects.get(pk=loanId)

        Amortization.objects.filter(loan_id=loanId,amortizationStatus__id=4).delete()#DRAFT
        
        #loan principal balance

         
        cycle = interestPaymentCycle
            
        schedules = int(termDays)/int(cycle)

        loan.latestPayment = loan.getLatestPayment()

        if loan.latestPayment:
            loanAmount = loan.latestPayment.outStandingBalance 
        else:
            loanAmount = loan.amount
         

        pmt = PMT()
     
        # loanAmount = loan.amount
        print(loanAmount)
        
        # days =  loan.term.paymentPeriod.paymentCycle - delta.days
        days =  cycle
        noOfPaymentSchedules = schedules
        print(noOfPaymentSchedules  )
        schedule = dateStart    + timezone.timedelta(days=days) 
       
       
        amortization = Amortization( 
            loan = loan,
            dateReleased = dateStart,
            amortizationStatus = AmortizationStatus.objects.get(pk=4),#DRAFT
            createdBy = request.user,
            schedules = schedules,
            termDays = termDays,
            cycle =cycle
        )

        amortization.save()
        if principalPaymentCycle == interestPaymentCycle:
            for i in range(int(noOfPaymentSchedules)):

                pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,termDays,noOfPaymentSchedules,noOfPaymentSchedules - i)
                lastPayment = schedule - timezone.timedelta(days=cycle)
    
                dayTillCutOff = cycle - int(lastPayment.strftime ('%d') ) 

                accruedInterest = (int(pmt.principal)) * (loan.interestRate.interestRate/100) *  dayTillCutOff/360

                amortizationItem = AmortizationItem(
                    schedule = schedule,
                    amortization = amortization,
                    days= days,
                    principal = pmt.principal,
                    deductAccruedInterest =  pmt.interest - accruedInterest,
                    accruedInterest = accruedInterest,
                    interest = pmt.interest,
                    additionalInterest = 0,
                    penalty = 0,
                    vat = 0,
                    total = pmt.payment,
                    principalBalance = pmt.nextStartingValue,
                    amortizationStatus = AmortizationStatus.objects.get(pk=1), 
                )
                amortizationItem.save()
                
    

                schedule = schedule + timezone.timedelta(days=days)
                
            

                loanAmount = pmt.nextStartingValue
        else:
            noOfPrincipalPaymentSchedules = loan.term.days / principalPaymentCycle
    # noOfPaymentSchedules = loan.term.days / loan.term.paymentPeriod.paymentCycle
            noOfInterestPaymentSchedules = loan.term.days / interestPaymentCycle

            if noOfPrincipalPaymentSchedules > noOfInterestPaymentSchedules:
            
                noOfPaymentSchedules = noOfPrincipalPaymentSchedules

            else:
                noOfPaymentSchedules = noOfInterestPaymentSchedules

            pmtInterest = PMT()
            currentCycle = 1
            if loan.latestPayment:
                interestLoan = loan.latestPayment.outStandingBalance 
            else:
                interestLoan = loan.amount
             

            for i in range(int(noOfPaymentSchedules)):

                pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
                principaEntry = 0
                pmtInterest = pmtInterest.getPayment(interestLoan,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)
                if (cycle  *  (i+1)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle) : 
                # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):
                    
                    # pmtPrincipal = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPrincipalPaymentSchedules,noOfPrincipalPaymentSchedules - i)

                    principaEntry = int(loan.amount) / noOfPrincipalPaymentSchedules
                print(i)
                lastPayment = schedule - timezone.timedelta(days=cycle)
    
                dayTillCutOff = cycle - int(timezone.localtime(lastPayment).strftime ('%d') ) 

                accruedInterest = (int(pmt.principal)) * (loan.interestRate.interestRate/100) *  dayTillCutOff/360

                amortizationItem = AmortizationItem(
                    schedule = schedule,
                    amortization = amortization,
                    days= cycle,
                    principal = principaEntry,
                    deductAccruedInterest =  pmtInterest.interest - accruedInterest,
                    accruedInterest = accruedInterest,
                    interest = pmtInterest.interest,
                    additionalInterest = 0,
                    penalty = 0,
                    vat = 0,
                    total = int(principaEntry) + pmtInterest.interest,
                    principalBalance = pmt.nextStartingValue,
                    amortizationStatus = AmortizationStatus.objects.get(pk=1), 
                )
                amortizationItem.save()

                schedule = schedule + timezone.timedelta(days=cycle)
                loanAmount = pmt.nextStartingValue

                if (cycle  *  (i+1)) == (loan.term.principalPaymentPeriod.paymentCycle * currentCycle) : 
                # if i+1 == int(noOfPaymentSchedules)/ int(noOfPrincipalPaymentSchedules):
                    # loanAmount = pmt.nextStartingValue
                    
                    currentCycle  = currentCycle + 1
                    interestLoan = int(principaEntry)
        
        
        # excludeWeekends(amortization.amortizationItems)
        return Response({
            'success':'true',
            'message': 'Restructured Amortization Generated'
        },status= status.HTTP_202_ACCEPTED)
 
        # return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)



class CalculatePMTView(views.APIView):
    
    # @method_decorator(csrf_protect) 

    def post(self,request):
        params = request.data.get("params") 
        
        print(params)
        datePayment = datetime.strptime(params["datePayment"], '%m/%d/%Y')  
        dateSchedule = datetime.strptime(params["dateSchedule"], '%m/%d/%Y')  
        loanId = params["loanId"]

        loan = Loan.objects.get(pk=loanId)

        loan.latestAmortization = loan.getLatestAmortization() 
        loan.currentAmortizationItem = loan.getCurrentAmortizationItem()
        # noOfPaymentSchedules = loan.latestAmortization.schedules
        cycle = loan.latestAmortization.cycle
        termDays = loan.latestAmortization.termDays
        loanAmount = loan.amount
        latestPayment = loan.getLatestPayment()
        if latestPayment: 
            loanAmount = latestPayment.outStandingBalance 

        pmt = PMT()
     
        # loanAmount = loan.amount
        print(loanAmount)
        delta = dateSchedule - datePayment
        # days =  loan.term.paymentPeriod.paymentCycle - delta.days
        days =  cycle 
        noOfPaymentSchedules = termDays / days
        # print(noOfPaymentSchedules  )
        print(cycle)
        print("asdasd")
        print(noOfPaymentSchedules)
        pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,termDays,noOfPaymentSchedules,noOfPaymentSchedules - (loan.latestAmortization.amortizationItems.filter(amortizationStatus__name='PAID').count()    ))
        print(delta.days)
        days =  cycle - delta.days
        daysExceed = days - cycle
        
        
        daysAdvanced = cycle - days 
        
        interest = 0

        # principal = pmt.principal
        principal = loan.currentAmortizationItem.principal
        interest = loan.currentAmortizationItem.interest

        payment = pmt.payment
        print(principal)


        if daysAdvanced < 0:
            daysAdvanced = 0
            # interest = pmt.interest
            # interest =loanAmount * (loan.interestRate.interestRate/100) * days/360
            totalToPay = principal + interest
        else:
            print(days)
            interest =  interest - (loanAmount * (loan.interestRate.interestRate/100) * daysAdvanced/360)
            totalToPay = principal + interest
            # pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,days,noOfPaymentSchedules,noOfPaymentSchedules - loan.payments.count())

        # principalBalance =pmt.nextStartingValue
        principalBalance = loan.currentAmortizationItem.principalBalance

        totalDays = 0
        # payments = loan.latestAmortization. 
        if latestPayment:
            if latestPayment.balance >= 1:
                principal = latestPayment.balance
                interest = latestPayment.interest - latestPayment.interestPayment
                totalToPay = principal + interest
                loanAmount = latestPayment.balance
                payment = principal
                principalBalance = latestPayment.principalBalance

            if latestPayment.overPayment >=1:
                principal =  pmt.principal - latestPayment.overPayment
                totalToPay = principal + interest

            diff =  datePayment.replace(tzinfo=None) - latestPayment.datePayment.replace(tzinfo=None) 

            totalDays = diff.days 
            print('totalDays')
            
            print(totalDays)
            dayTillCutOff = totalDays - int(datePayment.replace(tzinfo=None).strftime ('%d') )     
        
        else:
             
            totalDays = days   

        
            dayTillCutOff = totalDays - int(datePayment.replace(tzinfo=None).strftime ('%d') )   

        print( int(datePayment.replace(tzinfo=None).strftime ('%d') )  )
        print('dayTillCutOff')
        print(dayTillCutOff)
        accruedInterest = (Decimal(pmt.principal + pmt.nextStartingValue)) * (loan.interestRate.interestRate/100) *  dayTillCutOff/360
        print(pmt.principal)
        additionalInterest = 0
        print("accruedInterest")
        # interest =  interest - (loanAmount * (loan.interestRate.interestRate/100) * daysAdvanced/360)
        if daysExceed < 0:
            daysExceed = 0

        if daysExceed > 0:
            additionalInterest = (Decimal(totalToPay) )  *  (loan.interestRate.interestRate/100) * daysExceed/360

        penalty = 0
        if additionalInterest>0:
            penalty =  ( Decimal(totalToPay) + Decimal(float(additionalInterest)))  *  Decimal(12/100) * daysExceed/360

        totalToPayWithPenalty= (totalToPay) + (additionalInterest) + (penalty)
        totalInterest = interest + additionalInterest
        
        
        return Response({
            'datePayment':datePayment,
            'dateSchedule':dateSchedule,  
            'days': days,
            'principal':principal,
            'accruedInterest':accruedInterest,
            'interest':interest,
            'totalInterest':totalInterest,
            'additionalInterest':additionalInterest, 
            'daysExceed':daysExceed,
            'daysAdvanced':daysAdvanced,
            'penalty':penalty, 
            'totalToPay':totalToPay,
            'totalToPayWithPenalty':totalToPayWithPenalty,
            'status': 'Accepted',
            'principalBalance':principalBalance,
            'message': 'PMT Calculated'
        },status= status.HTTP_202_ACCEPTED)
 
        # return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)


    

class LoanReleasedView(views.APIView):
    
    # @method_decorator(csrf_protect)
 

    def post(self,request): 
        documentid = request.data.get("documentid") 
        print(documentid)
        if documentid:  
            document = Document.objects.get(pk=documentid)
            document.dateApproved = timezone.now()
            document.save()


            loan = document.loan

            loan.dateReleased = timezone.now() 
           
            loan.loanStatus= LoanStatus.objects.get(pk=2) #CURRENT
            loan.save()
        
            if loan.term.principalPaymentPeriod == loan.term.interestPaymentPeriod:
 
                generateAmortizationSchedule(loan,request)
            else:
                generateUnevenAmortizationSchedule(loan,request)

           

            return Response({
                'status': 'Accepted',
                'message': 'Loan Updated'
            },status= status.HTTP_202_ACCEPTED)
 
        return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)


class CheckPermissionView(views.APIView):
    
    # @method_decorator(csrf_protect) 
    def post(self,request):
        

        subProcessId = request.data.get("subProcessId") 


        # subProcessId = request.data.get("subProcessId") 
         
        if subProcessId:  
            subProcess = SubProcess.objects.get(pk=subProcessId)
            
            allPositions = []
                 
            for step in subProcess.steps.all():
                for position in step.positions.all():

                    allPositions.append(position.id)
                    
                # subProcess.positions
            
            # subProcess.positions = allPositions
          
             
            currentUser = CustomUser.objects.get(username=request.user)

            # currentUser = Custo

            subProcess.positions = Position.objects.filter(id__in=allPositions)
            
            position = currentUser.getPosition()
            if position == 'ADMIN':
                return Response({
                    'status': 'Accepted', 
                    'permission':True
                },status= status.HTTP_202_ACCEPTED)

            if  position in allPositions:  
                return Response({
                    'status': 'Accepted', 
                    'permission':True
                },status= status.HTTP_202_ACCEPTED)


            return Response({
            'status': 'Accepted', 
            'permission':False
        },status= status.HTTP_202_ACCEPTED)
        return Response({'error':'Error on checking permissions'},status.HTTP_400_BAD_REQUEST)


    
    

class SubProcessViewSet(ModelViewSet):
    queryset = SubProcess.objects.all()
    serializer_class = SubProcessSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):


    
        queryset = SubProcess.objects.order_by('id')
        borrowerId = self.request.query_params.get('borrowerId', None)
        subProcessId = self.request.query_params.get('subProcessId', None)
        
        subProcessName = self.request.query_params.get('subProcessName', None)
     
        if subProcessId is not None:
            queryset = queryset.filter(id=subProcessId)

            
        if subProcessName is not None:
            queryset = queryset.filter(name=subProcessName)

        if borrowerId is not None:

            borrower = Borrower.objects.get(pk=borrowerId)
            
            for subProcess in queryset:
                subProcess.canCreateNewFile = subProcess.isCanCreateNewFile(borrower)
                parentLastDocument = subProcess.getParentLastDocument(borrower)
                
                 

                if parentLastDocument:
                    if parentLastDocument.loan:
                        subProcess.parentLastDocumentLoan = parentLastDocument.loan
 
                    if parentLastDocument.creditLine:
                        subProcess.parentLastDocumentCreditLine = parentLastDocument.creditLine
                        subProcess.parentLastDocumentCreditLine.totalAvailment = subProcess.parentLastDocumentCreditLine.getTotalAvailment()
                        subProcess.parentLastDocumentCreditLine.remainingCreditLine = subProcess.parentLastDocumentCreditLine.getRemainingCreditLine()
 


        for subProcess in queryset:
                
                allPositions = []
                 
                for step in subProcess.steps.all():
                    for position in step.positions.all():

                        allPositions.append(position.id)
                        
                    # subProcess.positions
                
                # subProcess.positions = allPositions
                subProcess.positions = Position.objects.filter(id__in=allPositions)
                 

          

        return queryset


class StepViewSet(ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer 
    permission_classes = (permissions.IsAuthenticated, )
    
    def get_queryset(self):
        queryset = Step.objects.exclude(isDeleted=True).order_by('order')
        stepId = self.request.query_params.get('stepId', None)
      
        print(stepId)
        if stepId is not None:
            currentStep = Step.objects.get(pk=stepId)
            process = self.request.query_params.get('process', None)
            queryset=queryset.filter(subProcess = currentStep.subProcess)

            if process is not None:
                 

                if process == 'last':
                    step = Step.objects.get(id=stepId)
                    queryset = queryset.filter(order__gte=step.order).order_by('-order')[:1]

                elif process == 'current':
                    step = Step.objects.get(id=stepId)
                    queryset = queryset.filter(order__gt=step.order).order_by('order')[:1]

                elif process == 'next':                    
                    step = Step.objects.get(id=stepId)                
                    current = Step.objects.filter(order__gt=step.order).order_by('order').first()
                    queryset = queryset.filter(order__gt=step.order).exclude(pk=current.pk).order_by('order')[:1]
            else: 
                queryset = queryset.filter(id=stepId)
        
        return queryset.prefetch_related('outputs','positions')

class OutputViewSet(ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Output.objects.annotate(
            stepName=F('step__name'), 
            stepStatus=F('step__status'), 
        ).order_by('id')
        outputID = self.request.query_params.get('outputID', None)

        if outputID is not None:
            queryset = queryset.filter(id=outputID)

        return queryset


class StatusViewSet(ModelViewSet):
    queryset = Statuses.objects.all()
    serializer_class = StatusSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Statuses.objects.order_by('id')
        statusId = self.request.query_params.get('statusId', None)

        if statusId is not None:
            queryset = queryset.filter(id=statusId)

        return queryset

class StepRequirementViewSet(ModelViewSet):
    queryset = StepRequirement.objects.all()
    serializer_class = StepRequirementSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = StepRequirement.objects.annotate(
            isRequiredText=Case(
                    When(isRequired=True, then=V('Required')), 
                    default=V('Not Required'),
                    output_field=CharField(),
        ),
            stepName=F('step__name'),  
        ).order_by('id')


        stepId   = self.request.query_params.get('stepId', None)

        
        if stepId is not None:
            queryset = queryset.filter(step__id=stepId)
        else:        
            stepRequirementId = self.request.query_params.get('stepRequirementId', None)

            if stepRequirementId is not None:
                queryset = queryset.filter(id=stepRequirementId)

        return queryset.prefetch_related("stepRequirementAttachments")


class StepRequirementAttachmentViewSet(ModelViewSet):
    queryset = StepRequirementAttachment.objects.all()
    serializer_class = StepRequirementAttachmentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = StepRequirementAttachment.objects.annotate(
            stepRequirementName=F('stepRequirement__name'), 
        ).order_by('id')

        stepRequirementId = self.request.query_params.get('stepRequirementId', None)
        

        if stepRequirementId is not None:

            documentId = self.request.query_params.get('documentId', None)
            
            if documentId is not None:
                queryset = queryset.filter(stepRequirement__id=stepRequirementId,document__id=documentId) 
            
        else:
            stepRequirementAttachmentId = self.request.query_params.get('stepRequirementAttachmentId', None)

            if stepRequirementAttachmentId is not None:
                queryset = queryset.filter(id=stepRequirementAttachmentId)

        return queryset



#----Process


class ProcessRequirementViewSet(ModelViewSet):
    queryset = ProcessRequirement.objects.all()
    serializer_class = ProcessRequirementSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = ProcessRequirement.objects.annotate(
            isRequiredText=Case(
                    When(isRequired=True, then=V('Required')), 
                    default=V('Not Required'),
                    output_field=CharField(),
        ),
            processName=F('subProcess__name'),  
        ).order_by('id')


        subProcessId   = self.request.query_params.get('subProcessId', None)

        
        if subProcessId is not None:
            queryset = queryset.filter(subProcess__id=subProcessId)
        else:        
            processRequirementId = self.request.query_params.get('processRequirementId', None)

            if processRequirementId is not None:
                queryset = queryset.filter(id=processRequirementId)

        return queryset.prefetch_related("processRequirementAttachments")


class ProcessRequirementAttachmentViewSet(ModelViewSet):
    queryset = ProcessRequirementAttachment.objects.all()
    serializer_class = ProcessRequirementAttachmentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = ProcessRequirementAttachment.objects.annotate(
            processRequirementName=F('processRequirement__name'), 
            committeeName=Concat(F('committee__firstname'),V(' '),F('committee__middlename'),V(' '),F('committee__lastname')),
        ).order_by('id')

        processRequirementId = self.request.query_params.get('processRequirementId', None)
        

        if processRequirementId is not None:

            documentId = self.request.query_params.get('documentId', None)
            
            if documentId is not None:
                queryset = queryset.filter(processRequirement__id=processRequirementId,document__id=documentId) 
            
        else:
            processRequirementAttachmentId = self.request.query_params.get('processRequirementAttachmentId', None)

            if processRequirementAttachmentId is not None:
                queryset = queryset.filter(id=processRequirementAttachmentId)

        return queryset