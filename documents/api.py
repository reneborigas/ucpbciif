from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func,CharField,Min,Max
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from committees.models import Note
from processes.models import Statuses,SubProcess

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):  
        
        queryset = Document.objects.prefetch_related( 
               Prefetch( 'documentMovements',queryset=DocumentMovement.objects.order_by('-dateCreated'))
              ).annotate(
            documentCode=Concat(F('subProcess__code'),F('id'), output_field=CharField()),
            subProcessName=F('subProcess__name'),
            documentTypeName=F('documentType__name'), 
            borrowerName=F('borrower__cooperative__name'), 
            lastDocumentMovementId=Max( 'documentMovements__id'),   
            subProcessId=F('subProcess__id')
        ) .exclude(isDeleted=True).order_by('-id')

       
        documentId = self.request.query_params.get('documentId', None)
        subProcessName = self.request.query_params.get('subProcessName', None)
        subProcessId = self.request.query_params.get('subProcessId', None)
         
         
        if documentId is not None:
            queryset = queryset.filter(id=documentId)

        if subProcessName is not None:
            queryset = queryset.filter(subProcessName=subProcessName)

        if subProcessId is not None:
            queryset = queryset.filter(subProcess=subProcessId)

        return queryset.prefetch_related('notes')


 
class DocumentMovementViewSet(ModelViewSet):
    queryset = DocumentMovement.objects.all()
    serializer_class = DocumentMovementSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        
        queryset = DocumentMovement.objects.annotate(
            documentId=F('document_id'), 
            outputName=F('output__name'),
            outputId=F('output_id'), 
            stepId=F('step_id'),
            committeeName=Concat(F('committee__firstname'),V(' '),F('committee__middlename'),V(' '),F('committee__lastname')),
            statusName=F('status__name'), 
        ).exclude(isDeleted=True).order_by('-id')
       

        documentId = self.request.query_params.get('documentId', None)
      
       
        process = self.request.query_params.get('process', None)
      
        

        if documentId is not None:
       
            if process is not None:
                if process =='last':
                    queryset = queryset.filter(document_id=documentId).order_by('-dateCreated')[:1]
       
            else:
                queryset = queryset.filter(document_id=documentId)

        

        return queryset.prefetch_related(Prefetch('output',Output.objects.all()))

 