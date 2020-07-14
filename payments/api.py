from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

 

    
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

        if paymentId is not None:
            queryset = queryset.filter(id=paymentId) 
        return queryset
 