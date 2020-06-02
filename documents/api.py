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
<<<<<<< HEAD
        documentType = self.request.query_params.get('documentType', None)
        subProcessName = self.request.query_params.get('subProcessName', None)
=======
>>>>>>> 687ac4dab1d8ab55907f318413d1bba143e84367

        if documentId is not None:
            queryset = queryset.filter(id=documentId)

<<<<<<< HEAD
        if documentType is not None:
            queryset = queryset.filter(documentType=documentType)

        if subProcessName is not None:
            queryset = queryset.filter(subProcessName=subProcessName)

        print(documentType)
=======
>>>>>>> 687ac4dab1d8ab55907f318413d1bba143e84367
        return queryset
