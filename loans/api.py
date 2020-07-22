from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

from borrowers.models import Borrower


class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Loan.objects.order_by('id').exclude(isDeleted=True).annotate(termName=F('term__name'),loanProgramName=F('loanProgram__name')).prefetch_related(Prefetch( 'amortizations',queryset=Amortization.objects.order_by('-id')),)
        loanId = self.request.query_params.get('loanId', None)
        borrowerId = self.request.query_params.get('borrowerId', None)
        status = self.request.query_params.get('status', None)

        if loanId is not None:
            queryset = queryset.filter(id=loanId)
        if borrowerId is not None:
            queryset = queryset.filter(borrower__borrowerId=borrowerId)

        if status is not None:
            queryset = queryset.filter(status__name=status)

        for loan in queryset:
            loan.totalAmortizationInterest = loan.getTotalAmortizationInterest
            loan.totalAmortizationPayment = loan.getTotalAmortizationPayment
            loan.latestAmortization = loan.getLatestAmortization 
            loan.outStandingBalance = loan.getOutstandingBalance
            loan.currentAmortizationItem = loan.getCurrentAmortizationItem
            loan.totalObligations = loan.getTotalObligations
            loan.latestPayment = loan.getLatestPayment
            loan.totalPayment = loan.getTotalPayment
            loan.interestBalance = loan.getInterestBalance

            for amortization in loan.amortizations.all() : 

                amortization.totalAmortizationInterest = amortization.getTotalAmortizationInterest
                amortization.totalObligations = amortization.getTotalObligations


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
            
        return queryset

class CreditLineViewSet(ModelViewSet):
    
    queryset = CreditLine.objects.all()
    serializer_class = CreditLineSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = CreditLine.objects.order_by('id').annotate(termName=F('term__name'),loanProgramName=F('loanProgram__name'))
        creditLineId = self.request.query_params.get('creditlineid', None)
      
        if creditLineId is not None:
            queryset = queryset.filter(id=creditLineId)
            for creditLine in queryset:
                creditLine.remainingCreditLine = creditLine.getRemainingCreditLine()
 
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
