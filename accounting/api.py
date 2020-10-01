from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

class ChartOfAccountTypeViewSet(ModelViewSet):
    queryset = ChartOfAccountType.objects.exclude(isDeleted=True).order_by('id')
    serializer_class = ChartOfAccountTypeSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ChartOfAccountViewSet(ModelViewSet):
    queryset =  ChartOfAccount.objects.prefetch_related(
            'createdBy',
            'accountType',
        ).exclude(isDeleted=True).order_by('accountCode')
    serializer_class = ChartOfAccountSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = ChartOfAccount.objects.prefetch_related(
            'createdBy',
            'accountType',
        ).exclude(isDeleted=True).order_by('accountCode')

        id = self.request.query_params.get('id', None)

        if id is not None:
            queryset = queryset.filter(id=id)

        return queryset