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
        queryset = Loan.objects.order_by('id').annotate(termName=F('term__name'),loanProgramName=F('loanProgram__name'))
        loanId = self.request.query_params.get('loanId', None)

        if loanId is not None:
            queryset = queryset.filter(id=loanId)

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
