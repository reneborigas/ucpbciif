from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func,CharField
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat

from committees.models import Position
from borrowers.models import Borrower
from loans.models import CreditLine,Loan,Amortization
from documents.models import Document
from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from loans.models import Status
from django.utils import timezone


def generateAmortizationSchedule(loan,request):
    noOfItems = loan.term.days / loan.term.paymentPeriod.paymentCycle
    schedule = loan.dateReleased  + timezone.timedelta(days=loan.term.paymentPeriod.paymentCycle)
    
    for i in range(int(noOfItems)):
        amortization = Amortization(
            schedule = schedule,
            loan = loan,
            days= loan.term.paymentPeriod.paymentCycle,
            principal = 0,
            interest = 0,
            vat = 0,
            total = 0,
            principalBalance = 0,
            status = Status.objects.get(pk=1),
            createdBy = request.user
        )
        amortization.save()

        schedule = schedule + timezone.timedelta(days=loan.term.paymentPeriod.paymentCycle)


class CreditLineApprovedView(views.APIView):
    
    # @method_decorator(csrf_protect)
    def post(self,request):

        documentid = request.data.get("documentid") 
        if documentid:  
            document = Document.objects.get(pk=documentid)
            document.dateApproved = timezone.now()
            document.save()

            creditLine = document.creditLine
            creditLine.dateApproved = timezone.now()
            creditLine.dateExpired = timezone.now() + timezone.timedelta(days=365)


            creditLine.status= Status.objects.get(pk=6) #APPROVED
            creditLine.save()


            return Response({
                'status': 'Accepted',
                'message': 'Credit Line Updated'
            },status= status.HTTP_202_ACCEPTED)
 
        return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)

class LoanAvailmemtApprovedView(views.APIView):
    
    # @method_decorator(csrf_protect)
    def post(self,request):

        documentid = request.data.get("documentid") 
        print(documentid)
        if documentid:  
            document = Document.objects.get(pk=documentid)
            document.dateApproved = timezone.now()
            document.save()

            loan = document.loan
            loan.dateApproved = timezone.now() 

            loan.status= Status.objects.get(pk=6) #APPROVED
            loan.save()
    

            return Response({
                'status': 'Accepted',
                'message': 'Loan Updated'
            },status= status.HTTP_202_ACCEPTED)
 
        return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)

class LoanReleasedView(views.APIView):
    
    # @method_decorator(csrf_protect)


    

    def post(self,request):

        documentid = request.data.get("documentid") 
        print(documentid)
        if documentid:  
            document = Document.objects.get(pk=documentid)
            document.dateApproved = timezone.now()
            document.save()


            loan = document.loan
            loan.dateReleased = timezone.now() 

            loan.status= Status.objects.get(pk=6) #APPROVED
            loan.save()
            generateAmortizationSchedule(loan,request)

            return Response({
                'status': 'Accepted',
                'message': 'Loan Updated'
            },status= status.HTTP_202_ACCEPTED)
 
        return Response({'error':'Error on approving credit line'},status.HTTP_400_BAD_REQUEST)


    

class SubProcessViewSet(ModelViewSet):
    queryset = SubProcess.objects.all()
    serializer_class = SubProcessSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):


    
        queryset = SubProcess.objects.order_by('id')
        borrowerId = self.request.query_params.get('borrowerId', None)
        subProcessId = self.request.query_params.get('subProcessId', None)
        

        if subProcessId is not None:
            queryset = queryset.filter(id=subProcessId)

        if borrowerId is not None:

            borrower = Borrower.objects.get(pk=borrowerId)
            
            for subProcess in queryset:
                subProcess.canCreateNewFile = subProcess.isCanCreateNewFile(borrower)
                parentLastDocument = subProcess.getParentLastDocument(borrower)
               
                if parentLastDocument:
                    if parentLastDocument.loan:
                        subProcess.parentLastDocumentLoan = parentLastDocument.loan
 
                    if parentLastDocument.creditLine:
                        subProcess.parentLastDocumentCreditLine = parentLastDocument.creditLine
        
         
      
        return queryset


class StepViewSet(ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer 
    permission_classes = (permissions.IsAuthenticated, )
    
    def get_queryset(self):
        queryset = Step.objects.exclude(isDeleted=True).order_by('order')
        stepId = self.request.query_params.get('stepId', None)
      
        print(stepId)
        if stepId is not None:
            currentStep = Step.objects.get(pk=stepId)
            process = self.request.query_params.get('process', None)
            queryset=queryset.filter(subProcess = currentStep.subProcess)

            if process is not None:
                 

                if process == 'last':
                    step = Step.objects.get(id=stepId)
                    queryset = queryset.filter(order__gte=step.order).order_by('-order')[:1]

                elif process == 'current':
                    step = Step.objects.get(id=stepId)
                    queryset = queryset.filter(order__gt=step.order).order_by('order')[:1]

                elif process == 'next':                    
                    step = Step.objects.get(id=stepId)                
                    current = Step.objects.filter(order__gt=step.order).order_by('order').first()
                    queryset = queryset.filter(order__gt=step.order).exclude(pk=current.pk).order_by('order')[:1]
            else: 
                queryset = queryset.filter(id=stepId)
        
        return queryset.prefetch_related('outputs','position')

class OutputViewSet(ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Output.objects.annotate(
            stepName=F('step__name'), 
            stepStatus=F('step__status'), 
        ).order_by('id')
        outputID = self.request.query_params.get('outputID', None)

        if outputID is not None:
            queryset = queryset.filter(id=outputID)

        return queryset


class StatusViewSet(ModelViewSet):
    queryset = Statuses.objects.all()
    serializer_class = StatusSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Statuses.objects.order_by('id')
        statusId = self.request.query_params.get('statusId', None)

        if statusId is not None:
            queryset = queryset.filter(id=statusId)

        return queryset

class StepRequirementViewSet(ModelViewSet):
    queryset = StepRequirement.objects.all()
    serializer_class = StepRequirementSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = StepRequirement.objects.annotate(
            isRequiredText=Case(
                    When(isRequired=True, then=V('Required')), 
                    default=V('Not Required'),
                    output_field=CharField(),
        ),
            stepName=F('step__name'),  
        ).order_by('id')


        stepId   = self.request.query_params.get('stepId', None)

        
        if stepId is not None:
            queryset = queryset.filter(step__id=stepId)
        else:        
            stepRequirementId = self.request.query_params.get('stepRequirementId', None)

            if stepRequirementId is not None:
                queryset = queryset.filter(id=stepRequirementId)

        return queryset.prefetch_related("stepRequirementAttachments")


class StepRequirementAttachmentViewSet(ModelViewSet):
    queryset = StepRequirementAttachment.objects.all()
    serializer_class = StepRequirementAttachmentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = StepRequirementAttachment.objects.annotate(
            stepRequirementName=F('stepRequirement__name'), 
        ).order_by('id')

        stepRequirementId = self.request.query_params.get('stepRequirementId', None)
        

        if stepRequirementId is not None:

            documentId = self.request.query_params.get('documentId', None)
            
            if documentId is not None:
                queryset = queryset.filter(stepRequirement__id=stepRequirementId,document__id=documentId) 
            
        else:
            stepRequirementAttachmentId = self.request.query_params.get('stepRequirementAttachmentId', None)

            if stepRequirementAttachmentId is not None:
                queryset = queryset.filter(id=stepRequirementAttachmentId)

        return queryset



#----Process


class ProcessRequirementViewSet(ModelViewSet):
    queryset = ProcessRequirement.objects.all()
    serializer_class = ProcessRequirementSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = ProcessRequirement.objects.annotate(
            isRequiredText=Case(
                    When(isRequired=True, then=V('Required')), 
                    default=V('Not Required'),
                    output_field=CharField(),
        ),
            processName=F('subProcess__name'),  
        ).order_by('id')


        subProcessId   = self.request.query_params.get('subProcessId', None)

        
        if subProcessId is not None:
            queryset = queryset.filter(subProcess__id=subProcessId)
        else:        
            processRequirementId = self.request.query_params.get('processRequirementId', None)

            if processRequirementId is not None:
                queryset = queryset.filter(id=processRequirementId)

        return queryset.prefetch_related("processRequirementAttachments")


class ProcessRequirementAttachmentViewSet(ModelViewSet):
    queryset = ProcessRequirementAttachment.objects.all()
    serializer_class = ProcessRequirementAttachmentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = ProcessRequirementAttachment.objects.annotate(
            processRequirementName=F('processRequirement__name'), 
        ).order_by('id')

        processRequirementId = self.request.query_params.get('processRequirementId', None)
        

        if processRequirementId is not None:

            documentId = self.request.query_params.get('documentId', None)
            
            if documentId is not None:
                queryset = queryset.filter(processRequirement__id=processRequirementId,document__id=documentId) 
            
        else:
            processRequirementAttachmentId = self.request.query_params.get('processRequirementAttachmentId', None)

            if processRequirementAttachmentId is not None:
                queryset = queryset.filter(id=processRequirementAttachmentId)

        return queryset