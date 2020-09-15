from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func,CharField,Min,Max,Q
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from committees.models import Note
from processes.models import Statuses,SubProcess

from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

    

class GetDocumentFileName(views.APIView): 

    def post(self,request):

        code = request.data.get("code")  
         
        if code is None:
            code = 'ITM';

        document = Document.objects.all().order_by('-id').first()
         
        if not document:

            return Response({
                'status': 'Accepted',
                'fileName': code + '-' + '001'
            },status= status.HTTP_202_ACCEPTED)
 
         
        itemNumber = ''.join([n for n in document.name if n.isdigit()])
        
        itemNumber = int(itemNumber)  + 1
        itemNumber = str(itemNumber).zfill(3) 


        print(itemNumber) 
        return Response({
            'status': 'Accepted',
            'fileName': code + '-' + itemNumber
        },status= status.HTTP_202_ACCEPTED)

        return Response({'error':'Error on approving generating document filename'},status.HTTP_400_BAD_REQUEST)



class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):  
        
        queryset = Document.objects.prefetch_related( 'notes',
            Prefetch( 'documentMovements',queryset=DocumentMovement.objects.annotate(
                documentId=F('document_id'), 
                outputName=F('output__name'),
                outputId=F('output_id'), 
                stepId=F('step_id'),
                committeeName=Concat(F('committee__firstname'),V(' '),F('committee__middlename'),V(' '),F('committee__lastname')),
                statusName=F('status__name'), 
            ).order_by('-dateCreated'))
              ).annotate(
                termName=F('loan__term__name'),
                documentCode=Concat(F('subProcess__code'),F('id'), output_field=CharField()),
                subProcessName=F('subProcess__name'),
                documentTypeName=F('documentType__name'), 
                # borrowerName=F('borrower__cooperative__name'), 
                borrowerName=Case(
                    When(Q(borrower__recordType='BD'),then=F('borrower__business__tradeName')),
                    When(Q(borrower__recordType='ID'),then=Concat(F('borrower__individual__firstname'),V(' '),F('borrower__individual__middlename'),V(' '),F('borrower__individual__lastname')))
                ),
                lastDocumentMovementId=Max( 'documentMovements__id'),   
                subProcessId=F('subProcess__id')
            ) .exclude(isDeleted=True).order_by('-id')         
       
        documentId = self.request.query_params.get('documentId', None)
        subProcessName = self.request.query_params.get('subProcessName', None)
        subProcessId = self.request.query_params.get('subProcessId', None)
        loanId = self.request.query_params.get('loanId', None)
        credtiLineId = self.request.query_params.get('credtiLineId', None)
        
         
        if documentId is not None:
            queryset = queryset.filter(id=documentId)

        if loanId is not None:
            queryset = queryset.filter(loan__id=loanId)

        if credtiLineId is not None:
            queryset = queryset.filter(creditLine__id=credtiLineId)
        
        if subProcessName is not None:
            queryset = queryset.filter(subProcessName=subProcessName)

        if subProcessId is not None:
             
            queryset = queryset.filter(subProcessId=subProcessId)

        for document in queryset:
            document.currentStatus = document.getCurrentStatus() 
            print(document.currentStatus ) 
                 
            if  document.loan:
                document.loan.totalAmortizationInterest =  document.loan.getTotalAmortizationInterest
                document.loan.totalAmortizationPayment =  document.loan.getTotalAmortizationPayment
                document.loan.latestAmortization = document.loan.getLatestAmortization
            if document.creditLine: 
                document.creditLine.remainingCreditLine = document.creditLine.getRemainingCreditLine()
                
        return queryset

 
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

 