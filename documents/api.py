from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Document.objects.annotate(
          
            subProcessName=F('subProcess__name'),
            documentTypeName=F('documentType__name'),
            borrowerName=F('borrower__cooperative__name'),
        ).exclude(isDeleted=True).order_by('-id')
       

        documentId = self.request.query_params.get('documentId', None)
      
        subProcessName = self.request.query_params.get('subProcessName', None)


        if documentId is not None:
            queryset = queryset.filter(id=documentId)

        if subProcessName is not None:
            queryset = queryset.filter(subProcessName=subProcessName)

        return queryset

 
