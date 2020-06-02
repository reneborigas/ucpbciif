from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat


class CommitteeViewSet(ModelViewSet):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Committee.objects.annotate(
            committeeName=Concat(F('firstname'),V(' '),F('middlename'),V(' '),F('lastname'))
        ).exclude(isDeleted=True).order_by('-id')
       

        committeId = self.request.query_params.get('committeeId', None)
      
       
        if committeId is not None:
            queryset = queryset.filter(id=committeId)

       
 

        return queryset
