from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

class CheckViewSet(ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Check.objects.annotate(
            checkStatusText=F('checkStatus__name')
        ).order_by('id')
        checkId = self.request.query_params.get('checkId', None)

        if checkId is not None:
            queryset = queryset.filter(id=checkId) 

        return queryset


class CheckStatusViewSet(ModelViewSet):
    queryset = CheckStatus.objects.all()
    serializer_class = CheckStatusSerializer 
    permission_classes = (permissions.IsAuthenticated, )
    
    
class PaymentStatusViewSet(ModelViewSet):
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = PaymentStatus.objects.order_by('id')
        paymentStatusId = self.request.query_params.get('paymentStatusId', None)

        if paymentStatusId is not None:
            queryset = queryset.filter(id=paymentStatusId) 

        return queryset

class PaymentTypeViewSet(ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = PaymentType.objects.order_by('id')
        paymentTypeId = self.request.query_params.get('paymentTypeId', None)

        if paymentTypeId is not None:
            queryset = queryset.filter(id=paymentTypeId) 

        return queryset
 
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Payment.objects.order_by('id')
        paymentId = self.request.query_params.get('paymentId', None)

        borrowerId = self.request.query_params.get('borrowerId', None)
        principalFrom = self.request.query_params.get('principalFrom', None)
        principalTo = self.request.query_params.get('principalTo', None)

        interestFrom = self.request.query_params.get('interestFrom', None)
        interestTo = self.request.query_params.get('interestTo', None)
        accruedInterestFrom = self.request.query_params.get('accruedInterestFrom', None)
        accruedInterestTo = self.request.query_params.get('accruedInterestTo', None)

        paymentDateFrom = self.request.query_params.get('paymentDateFrom', None)
        paymentDateTo = self.request.query_params.get('paymentDateTo', None)
        totalPaymentFrom = self.request.query_params.get('totalPaymentFrom', None)
        totalPaymentTo = self.request.query_params.get('totalPaymentTo', None)
        paymentType = self.request.query_params.get('paymentType', None)
        status = self.request.query_params.get('status', None)

        if paymentId is not None:
            queryset = queryset.filter(id=paymentId)
        
        if borrowerId is not None:
            queryset = queryset.filter(borrower__borrowerId=borrowerId)

        if principalFrom is not None and principalTo is not None:
            queryset=queryset.filter(principal__gte=principalFrom).filter(principal__lte=principalTo)
        
        if interestFrom is not None and interestTo is not None:
            queryset=queryset.filter(interestPayment__gte=interestFrom).filter(interestPayment__lte=interestTo)

        if accruedInterestFrom is not None and accruedInterestTo is not None:
            queryset=queryset.filter(accruedInterestPayment__gte=accruedInterestFrom).filter(accruedInterestPayment__lte=accruedInterestTo)

        if paymentDateFrom is not None and paymentDateTo is not None:
            queryset=queryset.filter(datePayment__date__gte=paymentDateFrom).filter(datePayment__date__lte=paymentDateTo)

        if totalPaymentFrom is not None and totalPaymentTo is not None:
            queryset=queryset.filter(total__gte=totalPaymentFrom).filter(total__lte=totalPaymentTo)

        if paymentType is not None:
            queryset = queryset.filter(paymentType__name=paymentType)

        if status is not None:
            queryset = queryset.filter(paymentStatus__name=status)

        return queryset
 