from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func, Q
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from datetime import datetime
from borrowers.models import Borrower
from payments.models import Payment

from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from processes.api import generateAmortizationSchedule,generateUnevenAmortizationSchedule
from decimal import Decimal

class GetDashboardDataView(views.APIView):
    
   

    def get(self,request): 

        # queryset = AmortizationItem.objects.order_by('-id')
        # maturing = self.request.query_params.get('maturing', None)


        borrower = Borrower.objects.exclude(isDeleted=True).all()
        



        #totalpaymentreceived
        totalPayments = 0
        payments = Payment.objects.all()

        if payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']:
            totalPayments =  payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']

         

        totalLoans = 0
        totalBalance = 0
        loans = Loan.objects.filter(loanStatus__id=2).all()
        
        if payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']:
            totalPayments =  payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']

        for loan in loans:
            latestAmortization = loan.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()

          
      
            if latestAmortization: 
                totalLoans = totalLoans + latestAmortization.amortizationItems.aggregate(totalObligations=Sum(F('principal') ))['totalObligations'] 

                totalBalance = totalBalance + latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment']  -  totalPayments
            else:
                totalLoans = totalLoans +  0
                totalBalance = totalBalance +  0 
 
         

        return Response({
                'borrowerCount': borrower.count(), 
                'totalPayments':totalPayments,
                'totalLoans':totalLoans,
                'totalBalance':totalBalance
                 
            },status= status.HTTP_202_ACCEPTED) 
            


        # return Response({'error':'Error on retrieving dashboard information'},status.HTTP_400_BAD_REQUEST)




class GetAmortizationItemsCalendarView(views.APIView):
   


    def get(self,request): 

        queryset = AmortizationItem.objects.order_by('-id')
        maturing = self.request.query_params.get('maturing', None)



        
        amortizationItems = []
        for amortizationItem in queryset:
            if(amortizationItem.isOnCurrentAmortization()):
                amortizationItems.append(amortizationItem.id)
        queryset = queryset.filter(id__in=amortizationItems) 
        if maturing is not None:
            amortizationItems = []
            for amortizationItem in queryset:
                if(amortizationItem.isMaturingAmortizationItem()):
                    amortizationItems.append(amortizationItem.id)
            

            queryset = queryset.filter(id__in=amortizationItems)



        for amortizationItem in queryset:
            amortizationItem.start =  amortizationItem.schedule  
            # amortizationItem.start =  amortizationItem.schedule + timezone.timedelta(days=1)
            # amortizationItem.className =  'fc-event-solid-danger fc-event-light'
            amortizationItem.description  = 'Due for LN' + str(amortizationItem.amortization.loan.id)
            amortizationItem.url = '/loans/' + str(amortizationItem.amortization.loan.id)
            amortizationItem.backgroundColor = '#0073e9'
            amortizationItem.title = 'Amortization: LN' + str(amortizationItem.amortization.loan.id)
            
            if amortizationItem.amortizationStatus.id == 1:
                amortizationItem.backgroundColor = '#ff0000'
                amortizationItem.title = 'Unpaid Amortization: LN' + str(amortizationItem.amortization.loan.id)
                amortizationItem.url = '/payments/' + str(amortizationItem.amortization.loan.id)


            if amortizationItem.amortizationStatus.id == 3: #Partiall
                amortizationItem.backgroundColor = '#ff0000'
                amortizationItem.title = 'Unpaid Balance for Amortization: LN' + str(amortizationItem.amortization.loan.id)
                amortizationItem.url = '/payments/' + str(amortizationItem.amortization.loan.id)


            

        # return Response({
        #         'start': 'Credit Line Updated', 
        #         'end': creditLine.id,
        #         'className': new_value
        #     },status= status.HTTP_202_ACCEPTED) 
        #  title: 'Conference',
        #     //         start: '2020-06-11',
        #     //         end: '2020-06-13',
        #     //         className: 'fc-event-solid-danger fc-event-light',
        #     //         description: 'Lorem ipsum dolor sit ctetur adipi scing',


        serializer = CalendarAmortizationItemSerializer(queryset, many=True)
        return Response(serializer.data)
          

class UpdateCreditLineView(views.APIView):
    
    # @method_decorator(csrf_protect) 
    def post(self,request):
        

        creditLineId = request.data.get("creditLineId") 
        # subProcessId = request.data.get("subProcessId") 
        new_value =''
        if creditLineId:  
          
            creditLine = CreditLine.objects.get(pk=creditLineId)
           
            purpose = request.data.get("purpose")  
            if purpose: 
                creditLine.purpose = purpose
                new_value = purpose
            security = request.data.get("security")  
            if security: 
                creditLine.security = security
                new_value = security
            creditLine.save()

            return Response({
                'message': 'Credit Line Updated', 
                'creditLine': creditLine.id,
                'new_value': new_value
            },status= status.HTTP_202_ACCEPTED) 


        return Response({'error':'Error on updating creditline'},status.HTTP_400_BAD_REQUEST)


class UpdateCreditLineView(views.APIView):
    
    # @method_decorator(csrf_protect) 
    def post(self,request):
        creditLineId = request.data.get("creditLineId") 
        new_value =''
        if creditLineId:  
            creditLine = CreditLine.objects.get(pk=creditLineId)
           
            purpose = request.data.get("purpose")  
            if purpose: 
                creditLine.purpose = purpose
                new_value = purpose
                creditLine.save()

            security = request.data.get("security")  
            if security: 
                creditLine.security = security
                new_value = security

                creditLine.save()
           

            return Response({
                'message': 'Credit LIne Updated', 
                'creditLine': creditLine.id,
                'new_value': new_value
            },status= status.HTTP_202_ACCEPTED) 

        return Response({'error':'Error on updating credit line'},status.HTTP_400_BAD_REQUEST)


class UpdateAmortizationItemView(views.APIView):
    
    # @method_decorator(csrf_protect) 
    def post(self,request):
        amortizationItemId = request.data.get("amortizationItemId") 
        print("etp")
        new_value =''
        if amortizationItemId:  
            amortizationItem = AmortizationItem.objects.get(pk=amortizationItemId)
           
            days = request.data.get("days")  
            if days: 
                amortizationItem.days = days
                new_value = days
                amortizationItem.save()

            schedule = request.data.get("schedule")  
            if schedule: 
                amortizationItem.schedule = datetime.strptime(schedule, '%m/%d/%Y')  
                new_value = schedule
                amortizationItem.save()
            
            accruedInterest = request.data.get("accruedInterest")  

            if accruedInterest is not None: 
                 
                amortizationItem.accruedInterest = accruedInterest 
                
                # amortizationItem.deductAccruedInterest = int(amortizationItem.interest)  - int(amortizationItem.accruedInterest)
                amortizationItem.interest =  int(amortizationItem.deductAccruedInterest)  + int(amortizationItem.accruedInterest)
                amortizationItem.total = int(amortizationItem.interest) + int(amortizationItem.principal)
                new_value = accruedInterest
                amortizationItem.save()
                # lastBalance = amortizationItem.amortization.loan.amount

                # for amortizationItem in amortizationItem.amortization.amortizationItems.all():
                #     amortizationItem.principalBalance = lastBalance - amortizationItem.total
                #     amortizationItem.save()
                #     lastBalance =  amortizationItem.principalBalance 

            interest = request.data.get("interest")  
            if interest is not None: 
                
                amortizationItem.deductAccruedInterest = float(interest)
                 
                amortizationItem.interest =  (float(amortizationItem.deductAccruedInterest))  + float(amortizationItem.accruedInterest)
                amortizationItem.total = float(amortizationItem.interest) + float(amortizationItem.principal)

                new_value = interest
                amortizationItem.save()
                # lastBalance = amortizationItem.amortization.loan.amount


                # for amortizationItem in amortizationItem.amortization.amortizationItems.all():
                #     amortizationItem.principalBalance = lastBalance - amortizationItem.total
                #     amortizationItem.save()
                #     lastBalance =  amortizationItem.principalBalance 

            principal = request.data.get("principal")  
            if principal is not None: 
                amortizationItem.principal = principal 
                amortizationItem.total = int(amortizationItem.interest) + int(amortizationItem.principal)

                new_value = principal
                amortizationItem.save()
                # lastBalance = amortizationItem.amortization.loan.amount

                # for amortizationItem in amortizationItem.amortization.amortizationItems.all():
                #     amortizationItem.principalBalance = lastBalance - amortizationItem.total
                #     amortizationItem.save()
                #     lastBalance =  amortizationItem.principalBalance 

            principalBalance = request.data.get("principalBalance")  
            if principalBalance is not None: 
                amortizationItem.principalBalance = principalBalance 
              
                new_value = principalBalance
                amortizationItem.save()
                # lastBalance = amortizationItem.amortization.loan.amount

                # for amortizationItem in amortizationItem.amortization.amortizationItems.all():
                #     amortizationItem.principalBalance = lastBalance - amortizationItem.total
                #     amortizationItem.save()
                #     lastBalance =  amortizationItem.principalBalance 



            return Response({
                'message': 'Amortization Item Updated', 
                'amortizationItem': amortizationItem.id,
                'new_value': new_value
            },status= status.HTTP_202_ACCEPTED) 

        return Response({'error':'Error on updating credit line'},status.HTTP_400_BAD_REQUEST)


class UpdateLoanView(views.APIView):
    
    # @method_decorator(csrf_protect) 
    def post(self,request):
        loanId = request.data.get("loanId") 
        new_value =''
        if loanId:  
            loan = Loan.objects.get(pk=loanId)
           
            purpose = request.data.get("purpose")  
            if purpose: 
                loan.purpose = purpose
                new_value = purpose
                loan.save()

            security = request.data.get("security")  
            if security: 
                loan.security = security
                new_value = security

                loan.save()

            term = request.data.get("term")
            if term:
                if not loan.term == Term.objects.get(id=term):
                    loan.term = Term.objects.get(id=term)
                    new_value = term

                    loan.save()

                    if loan.term.principalPaymentPeriod == loan.term.interestPaymentPeriod:
                        generateAmortizationSchedule(loan,request)
                    else:
                        generateUnevenAmortizationSchedule(loan,request)

            interest = request.data.get("interest")
            if interest:
                if not loan.interestRate == InterestRate.objects.get(id=interest):
                    loan.interestRate = InterestRate.objects.get(id=interest)
                    new_value = interest

                    loan.save()

                    if loan.term.principalPaymentPeriod == loan.term.interestPaymentPeriod:
                        generateAmortizationSchedule(loan,request)
                    else:
                        generateUnevenAmortizationSchedule(loan,request)


            dateReleased = request.data.get("dateReleased")  
            if dateReleased: 
                loan.dateReleased = dateReleased
                new_value = dateReleased
                loan.save()
                

                loan = Loan.objects.get(pk=loanId)
                schedule = loan.dateReleased +  timezone.timedelta(days=loan.term.interestPaymentPeriod.paymentCycle )
                amortization = loan.getLatestAmortization()
                amortization.dateReleased = loan.dateReleased    
                amortization.save()

                for amortizationItem in amortization.amortizationItems.all().order_by('id'):
                    amortizationItem.schedule = schedule
                   

                   
                    dayTillCutOff = loan.term.interestPaymentPeriod.paymentCycle - int(timezone.localtime(schedule).strftime ('%d') )  
                     
                    print("interest rates")
                   
                
                    accruedInterest = Decimal((amortizationItem.principal + amortizationItem.principalBalance) ) * (loan.interestRate.interestRate/100) *  dayTillCutOff/360
                    print(round(accruedInterest,2))
                    
                    amortizationItem.accruedInterest = accruedInterest
                    amortizationItem.deductAccruedInterest = amortizationItem.interest - accruedInterest
                    schedule = schedule + timezone.timedelta(days=loan.term.interestPaymentPeriod.paymentCycle)


                    amortizationItem.save()
                        
           

            return Response({
                'message': 'Loan Updated', 
                'loan': loan.id,
                'new_value': new_value
            },status= status.HTTP_202_ACCEPTED) 

        return Response({'error':'Error on updating loan'},status.HTTP_400_BAD_REQUEST)




class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Loan.objects.order_by('id').exclude(isDeleted=True).annotate(branch=F('borrower__branch__branchCode'),termName=F('term__name'),loanProgramName=F('loanProgram__name')).prefetch_related(Prefetch( 'amortizations',queryset=Amortization.objects.order_by('-id')),)
        loanId = self.request.query_params.get('loanId', None)
        creditLineId = self.request.query_params.get('creditLineId', None)
        borrowerId = self.request.query_params.get('borrowerId', None)
        status = self.request.query_params.get('status', None)
        dateFrom = self.request.query_params.get('dateFrom', None)
        dateTo = self.request.query_params.get('dateTo', None)
        loanFrom = self.request.query_params.get('loanFrom', None)
        loanTo = self.request.query_params.get('loanTo', None)
        loanTo = self.request.query_params.get('loanTo', None)
        loanProgram = self.request.query_params.get('loanProgram', None)
        loanProgramName = self.request.query_params.get('loanProgramName', None)
        
        if loanId is not None:
            queryset = queryset.filter(id=loanId)

        if creditLineId is not None:
            queryset = queryset.filter(creditLine__id=creditLineId)

        if borrowerId is not None:
            queryset = queryset.filter(borrower__borrowerId=borrowerId)

        if status is not None:
            queryset = queryset.filter( Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED')) 

        for loan in queryset:
            loan.totalAmortizationInterest = loan.getTotalAmortizationInterest
            loan.totalAmortizationAccruedInterest = loan.getTotalAmortizationAccruedInterest
              
            loan.totalDraftAmortizationInterest = loan.getTotalDraftAmortizationInterest  

            loan.loanTotalAmortizationPrincipal = loan.getTotalAmortizationPrincipal()
            loan.totalAmortizationPayment = loan.getTotalAmortizationPayment
            loan.latestAmortization = loan.getLatestAmortization()
            
          
            if loan.latestAmortization:
                loan.latestAmortization.totalAmortizationPrincipal = loan.latestAmortization.getTotalAmortizationPrincipal()

                for amortizationItem in loan.latestAmortization.amortizationItems.all() : 
                    amortizationItem.latestCheck = amortizationItem.getPDC()
                    
                    print(amortizationItem.latestCheck)
                

            loan.latestDraftAmortization = loan.getLatestDraftAmortization()  

            if loan.latestDraftAmortization:
                loan.latestDraftAmortization.totalAmortizationPrincipal = loan.latestDraftAmortization.getTotalAmortizationPrincipal()
                loan.latestDraftAmortization.totalAmortizationInterest = loan.latestDraftAmortization.getTotalAmortizationInterest()
                loan.latestDraftAmortization.totalAmortizationAccruedInterest = loan.latestDraftAmortization.getTotalAmortizationAccruedInterest()
                
                
            loan.outStandingBalance = loan.getOutstandingBalance
            loan.currentAmortizationItem = loan.getCurrentAmortizationItem()
            if loan.currentAmortizationItem:
                loan.currentAmortizationItem.latestCheck =  loan.currentAmortizationItem.getPDC()
            loan.lastAmortizationItem = loan.getLastAmortizationItem
            loan.totalObligations = loan.getTotalObligations
            loan.latestPayment = loan.getLatestPayment
            loan.totalPayment = loan.getTotalPayment
            loan.totalPrincipalPayment = loan.getTotalPrincipalPayment()
            loan.totalInterestPayment = loan.getTotaInterestPayment()
            loan.totalAccruedInterestPayment = loan.getTotalAccruedInterestPayment()
            loan.totalTotalInterestPayment = loan.getTotalTotalInterestPayment()
            loan.totalPenaltyPayment = loan.getTotalPenaltyPayment()
            loan.totalAdditionalInterestPayment = loan.getTotalAdditionalInterestPayment()

            loan.totalPrincipalBalance = loan.loanTotalAmortizationPrincipal  - loan.totalPrincipalPayment

            
            loan.interestBalance = loan.getInterestBalance

            # for amortizationItem in loan.latestAmortization.amortizationItems:
            #     amortizationItem.isItemPaid = amortizationItem.isPaid()

            for amortization in loan.amortizations.all() : 

                amortization.totalAmortizationInterest = amortization.getTotalAmortizationInterest
                amortization.totalAmortizationAccruedInterest = amortization.getTotalAmortizationAccruedInterest
                
                amortization.totalObligations = amortization.getTotalObligations
                amortization.totalAmortizationPrincipal = amortization.getTotalAmortizationPrincipal

        if dateFrom is not None and dateTo is not None:
            queryset=queryset.filter(dateReleased__date__gte=dateFrom).filter(dateReleased__date__lte=dateTo)

        if loanFrom is not None and loanTo is not None:
            queryset=queryset.filter(amount__gte=loanFrom).filter(amount__lte=loanTo)

        if loanProgram is not None:
            queryset=queryset.filter(loanProgram=loanProgram)

        if loanProgramName is not None:
            queryset=queryset.filter(loanProgram__name=loanProgramName)

        return queryset

class AmortizationViewSet(ModelViewSet):
    queryset = Amortization.objects.all()
    serializer_class = AmortizationSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Amortization.objects.order_by('-id')
        amortizationId = self.request.query_params.get('amortizationId', None)

        if amortizationId is not None:
            queryset = queryset.filter(id=amortizationId)

        for amortization in queryset:
            amortization.totalAmortizationInterest = amortization.getTotalAmortizationInterest
            amortization.totalObligations = amortization.getTotalObligations
            amortization.totalAmortizationPrincipal = amortization.getTotalAmortizationPrincipal
            # for amortizationItem in amortization.amortizationItems:
            #     amortizationItem.isItemPaid = amortizationItem.isPaid()


        return queryset


class AmortizationItemViewSet(ModelViewSet):
    queryset = AmortizationItem.objects.all()
    serializer_class = AmortizationItemSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = AmortizationItem.objects.order_by('-id')
        amortizationItemId = self.request.query_params.get('amortizationItemId', None)
        maturing = self.request.query_params.get('maturing', None)

        scheduleDateFrom = self.request.query_params.get('scheduleDateFrom',None)
        scheduleDateTo = self.request.query_params.get('scheduleDateTo',None)
        numberofDaysFrom = self.request.query_params.get('numberofDaysFrom',None)
        numberofDaysTo = self.request.query_params.get('numberofDaysTo',None)
        principalFrom = self.request.query_params.get('principalFrom',None)
        principalTo = self.request.query_params.get('principalTo',None)

        interestFrom = self.request.query_params.get('interestFrom',None)
        interestTo = self.request.query_params.get('interestTo',None)
        accruedInterestFrom = self.request.query_params.get('accruedInterestFrom',None)
        accruedInterestTo = self.request.query_params.get('accruedInterestTo',None)

        penaltyFrom = self.request.query_params.get('penaltyFrom',None)
        penaltyTo = self.request.query_params.get('penaltyTo',None)
        amortizationFrom = self.request.query_params.get('amortizationFrom',None)
        amortizationTo = self.request.query_params.get('amortizationTo',None)
        principalBalanceFrom = self.request.query_params.get('principalBalanceFrom',None)
        principalBalanceTo = self.request.query_params.get('principalBalanceTo',None)
        status = self.request.query_params.get('status',None)

        amortizationItems = []
        if amortizationItemId is not None:
            queryset = queryset.filter(id=amortizationItemId)

        for amortizationItem in queryset:
            if(amortizationItem.isOnCurrentAmortization()):
                amortizationItems.append(amortizationItem.id)

        queryset = queryset.filter(id__in=amortizationItems)    
         
        if maturing:
            amortizationItems=[]
            for amortizationItem in queryset:
                if(amortizationItem.isMaturingAmortizationItem()):
                    amortizationItems.append(amortizationItem.id)
             
            queryset = queryset.filter(id__in=amortizationItems)


        for amortizationItem in queryset:
            amortizationItem.totalPayment = amortizationItem.getTotalPayment
            amortizationItem.latestCheck = amortizationItem.getPDC()

        if status is not None:
            queryset = queryset.filter(status__name=status)

        if scheduleDateFrom is not None and scheduleDateTo is not None:
            queryset=queryset.filter(schedule__gte=scheduleDateFrom).filter(schedule__lte=scheduleDateTo)

        if numberofDaysFrom is not None and numberofDaysTo is not None:
            queryset=queryset.filter(days__gte=numberofDaysFrom).filter(days__lte=numberofDaysTo)

        if principalFrom is not None and principalTo is not None:
            queryset=queryset.filter(principal__gte=principalFrom).filter(principal__lte=principalTo)

        if interestFrom is not None and interestTo is not None:
            queryset=queryset.filter(interest__gte=interestFrom).filter(interest__lte=interestTo)

        if accruedInterestFrom is not None and accruedInterestTo is not None:
            queryset=queryset.filter(accruedInterest__gte=accruedInterestFrom).filter(accruedInterest__lte=accruedInterestTo)

        if penaltyFrom is not None and penaltyTo is not None:
            queryset=queryset.filter(penalty__gte=penaltyFrom).filter(penalty__lte=penaltyTo)

        if amortizationFrom is not None and amortizationTo is not None:
            queryset=queryset.filter(total__gte=amortizationFrom).filter(total__lte=amortizationTo)

        if principalBalanceFrom is not None and principalBalanceTo is not None:
            queryset=queryset.filter(principalBalance__gte=principalBalanceFrom).filter(principalBalance__lte=principalBalanceTo)

        
        return queryset

            

class CreditLineViewSet(ModelViewSet):
    
    queryset = CreditLine.objects.all()
    serializer_class = CreditLineSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = CreditLine.objects.order_by('id').annotate(termName=F('term__name'),loanProgramName=F('loanProgram__name'))
        # print(self.request.query_params)
        creditLineId = self.request.query_params.get('creditLineId', None)
        borrowerId = self.request.query_params.get('borrowerId', None)
        status = self.request.query_params.get('status', None)
        term = self.request.query_params.get('term', None)
        creditLineAmountFrom = self.request.query_params.get('creditLineAmountFrom', None)
        creditLineAmountTo = self.request.query_params.get('creditLineAmountTo', None)
        totalAvailmentFrom = self.request.query_params.get('totalAvailmentFrom', None)
        totalAvailmentTo = self.request.query_params.get('totalAvailmentTo', None)
        interestFrom = self.request.query_params.get('interestFrom', None)
        interestTo = self.request.query_params.get('interestTo', None)
        dateApprovedFrom = self.request.query_params.get('dateApprovedFrom', None)
        dateApprovedTo = self.request.query_params.get('dateApprovedTo', None)
        expiryDateFrom = self.request.query_params.get('expiryDateFrom', None)
        expiryDateTo = self.request.query_params.get('expiryDateTo', None)

        if status is not None:
            queryset = queryset.filter(status__name=status)

        if borrowerId is not None:
            queryset = queryset.filter(borrower=borrowerId)

        if creditLineId is not None:
            queryset = queryset.filter(id=creditLineId)

        if term is not None:
            queryset = queryset.filter(term=term)

        if creditLineAmountFrom is not None and creditLineAmountTo is not None:
            queryset=queryset.filter(amount__gte=creditLineAmountFrom).filter(amount__lte=creditLineAmountTo)

        if totalAvailmentFrom is not None and totalAvailmentTo is not None:
            creditLines = []
            for creditLine in queryset: 
                creditLine.totalAvailment = creditLine.getTotalAvailment() 
                if (int(creditLine.totalAvailment) >= int(totalAvailmentFrom)) and  (int(creditLine.totalAvailment) <= int(totalAvailmentTo)):
                    creditLines.append(creditLine.pk)

            queryset=queryset.filter(id__in=creditLines)

        if interestFrom is not None and interestTo is not None:
            queryset=queryset.filter(interestRate__interestRate__gte=interestFrom).filter(interestRate__interestRate__lte=interestTo)

        if dateApprovedFrom is not None and dateApprovedTo is not None:
            queryset=queryset.filter(dateApproved__date__gte=dateApprovedFrom).filter(dateApproved__date__lte=dateApprovedTo)

        if expiryDateFrom is not None and expiryDateTo is not None:
            queryset=queryset.filter(dateExpired__date__gte=expiryDateFrom).filter(dateExpired__date__lte=expiryDateTo)

        for creditLine in queryset:
            creditLine.remainingCreditLine = creditLine.getRemainingCreditLine()
            creditLine.totalAvailment = creditLine.getTotalAvailment() 

        return queryset

 
class LoanProgramViewSet(ModelViewSet):
    queryset = LoanProgram.objects.all()
    serializer_class = LoanProgramSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = LoanProgram.objects.order_by('id') 
        loanProgramId = self.request.query_params.get('loanProgramId', None)
        totalLoan = self.request.query_params.get('totalLoan', None)
        if loanProgramId is not None:
            queryset = queryset.filter(id=loanProgramId)
 

        borrowerId = self.request.query_params.get('borrowerId', None)
        print(borrowerId)
        if borrowerId is not None: 

            borrower = Borrower.objects.get(pk=borrowerId)
            
            for window in queryset:
                window.activeLoan = window.getActiveLoan(borrower)
                window.activeCreditLine = window.getActiveCreditline(borrower)
                window.totalAvailments = window.getTotalAvailments(borrower)


        print(totalLoan)
        
        for window in queryset:
            window.overallLoan = window.getOverallLoan() 
            if totalLoan is not None: 
                window.overallLoanPercentage = window.getOverallLoanPercentage(totalLoan)


        return queryset


class LoanProgramDistributionViewSet(ModelViewSet):
    queryset = LoanProgram.objects.all()
    serializer_class = LoanProgramDistributionSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = LoanProgram.objects.order_by('id') 
        loanProgramId = self.request.query_params.get('loanProgramId', None)
        totalLoan = self.request.query_params.get('totalLoan', None)
        if loanProgramId is not None:
            queryset = queryset.filter(id=loanProgramId)
 

        borrowerId = self.request.query_params.get('borrowerId', None)
        print(borrowerId)
        if borrowerId is not None: 

            borrower = Borrower.objects.get(pk=borrowerId)
            
            for window in queryset:
                window.activeLoan = window.getActiveLoan(borrower)
                window.activeCreditLine = window.getActiveCreditline(borrower)
                window.totalAvailments = window.getTotalAvailments(borrower)

 
        
        for window in queryset:
            window.overallLoan = window.getOverallLoan() 
            window.text = window.name
            if totalLoan is not None: 
                window.overallLoanPercentage = window.getOverallLoanPercentage(totalLoan)
                # values = []
                # values.append()
                window.values = [int(window.overallLoan)]


        return queryset


class TermViewSet(ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Term.objects.order_by('id').annotate(
            principalPaymentPeriodName=F('principalPaymentPeriod__name'),
            interestPaymentPeriodName=F('interestPaymentPeriod__name'),
        )
        termId = self.request.query_params.get('termId', None)

        if termId is not None:
            queryset = queryset.filter(id=termId)

        return queryset

class CRUDTermViewSet(ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = CRUDTermSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Term.objects.order_by('id')
        termId = self.request.query_params.get('termId', None)

        if termId is not None:
            queryset = queryset.filter(id=termId)

        return queryset

class InterestRateViewSet(ModelViewSet):
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = InterestRate.objects.order_by('interestRate')
        interestRateId = self.request.query_params.get('interestRateId', None)

        if interestRateId is not None:
            queryset = queryset.filter(id=interestRateId)
      
        return queryset


class PaymentPeriodViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = PaymentPeriodSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = PaymentPeriod.objects.order_by('id')
        paymentPeriodId = self.request.query_params.get('paymentPeriodId', None)

        if paymentPeriodId is not None:
            queryset = queryset.filter(id=paymentPeriodId)

        return queryset

class AmortizationStatusViewSet(ModelViewSet):
    queryset =  AmortizationStatus.objects.all()
    serializer_class = AmortizationStatusSerializer
    permission_classes = (permissions.IsAuthenticated, )

class LoanStatusViewSet(ModelViewSet):
    queryset =  LoanStatus.objects.all()
    serializer_class = LoanStatusSerializer
    permission_classes = (permissions.IsAuthenticated, )

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Status.objects.order_by('id')
        statusId = self.request.query_params.get('statusId', None)
        name = self.request.query_params.get('name', None)

        if statusId is not None:
            queryset = queryset.filter(id=statusId)

        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset
