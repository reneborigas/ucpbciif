from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from datetime import datetime
from borrowers.models import Borrower
from payments.models import Payment

from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

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
                totalLoans =  latestAmortization.amortizationItems.aggregate(totalObligations=Sum(F('total') ))['totalObligations']  
                totalBalance = latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment']  -  totalPayments
            else:
                totalLoans =  0
                totalBalance = 0

       

        

        
         

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
            amortizationItem.start =  amortizationItem.schedule.date() + timezone.timedelta(days=1)
         
            # amortizationItem.className =  'fc-event-solid-danger fc-event-light'
            amortizationItem.description  = 'Due for LN' + str(amortizationItem.amortization.loan.id)
            amortizationItem.url = '/loans/' + str(amortizationItem.amortization.loan.id)
            amortizationItem.backgroundColor = '#0073e9'
            amortizationItem.title = 'Amortization: LN' + str(amortizationItem.amortization.loan.id)
            
            if amortizationItem.amortizationStatus.id == 1:
                amortizationItem.backgroundColor = '#ff0000'
                amortizationItem.title = 'Unpaid Amortization: LN' + str(amortizationItem.amortization.loan.id)
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
                

            security = request.data.get("security")  
            if security: 
                loan.security = security
                new_value = security

            loan.save()

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
        queryset = Loan.objects.order_by('id').exclude(isDeleted=True).annotate(termName=F('term__name'),loanProgramName=F('loanProgram__name')).prefetch_related(Prefetch( 'amortizations',queryset=Amortization.objects.order_by('-id')),)
        loanId = self.request.query_params.get('loanId', None)
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

        if borrowerId is not None:
            queryset = queryset.filter(borrower__borrowerId=borrowerId)

        if status is not None:
            queryset = queryset.filter(loanStatus__name=status)

        for loan in queryset:
            loan.totalAmortizationInterest = loan.getTotalAmortizationInterest
            loan.totalAmortizationPayment = loan.getTotalAmortizationPayment
            loan.latestAmortization = loan.getLatestAmortization  
            loan.outStandingBalance = loan.getOutstandingBalance
            loan.currentAmortizationItem = loan.getCurrentAmortizationItem
            loan.lastAmortizationItem = loan.getLastAmortizationItem
            loan.totalObligations = loan.getTotalObligations
            loan.latestPayment = loan.getLatestPayment
            loan.totalPayment = loan.getTotalPayment
            loan.interestBalance = loan.getInterestBalance

            # for amortizationItem in loan.latestAmortization.amortizationItems:
            #     amortizationItem.isItemPaid = amortizationItem.isPaid()

            for amortization in loan.amortizations.all() : 

                amortization.totalAmortizationInterest = amortization.getTotalAmortizationInterest
                amortization.totalObligations = amortization.getTotalObligations

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
        # for amortizationItem in queryset:
        #     amortizationItem.isItemPaid = amortizationItem.isPaid()
        
        # fo
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

        return queryset

class TermViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = TermSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Term.objects.order_by('id').annotate(
              termName=Concat(F('name'),V(' '),F('paymentPeriod__name')),
        )
        termId = self.request.query_params.get('termId', None)

        if termId is not None:
            queryset = queryset.filter(id=termId)


      
        return queryset

class InterestRateViewSet(ModelViewSet):
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = InterestRate.objects.order_by('id')
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

# class AmortizationStatusViewSet(ModelViewSet):
#     queryset =  AmortizationStatus.objects.all()
#     serializer_class = AmortizationStatusSerializer
#     permission_classes = (permissions.IsAuthenticated, )

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
