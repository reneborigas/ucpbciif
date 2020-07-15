from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from documents.models import Document,DocumentMovement
from loans.models import Loan
class BorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Borrower.objects.prefetch_related('borrowerAttachments', Prefetch( 'documents',queryset=Document.objects.order_by('dateCreated')),
        Prefetch( 'loans',queryset=Loan.objects.order_by('dateReleased')),
            Prefetch('cooperative',Cooperative.objects.annotate(
                cooperativeTypeText=F('cooperativeType__name')
            ).all()),
            Prefetch( 'documents__documentMovements',queryset=DocumentMovement.objects.order_by('-dateCreated'))
        ).annotate(
            contactPersonName=Concat(F('contactPerson__firstname'),V(' '),F('contactPerson__middlename'),V(' '),F('contactPerson__lastname')),
            cooperativeName=F('cooperative__name'),
            tin=F('cooperative__tin'),
            address=F('cooperative__address'),
            phoneNo=F('cooperative__phoneNo'),
        ).exclude(isDeleted=True).order_by('borrowerId')
        borrowerId = self.request.query_params.get('borrowerId', None)
        loanProgramId = self.request.query_params.get('loanProgramId', None)

# .filter(status__name='RELEASED')
        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        for borrower in queryset:
            borrower.totalAvailments = borrower.getTotalAvailments
            borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance

            if loanProgramId is not None: 
                borrower.totalAvailmentPerProgram = borrower.getTotalAvailmentsPerProgram(loanProgramId)
                
        return queryset


class ContactPersonViewSet(ModelViewSet):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer #test comment
    permission_classes = (permissions.IsAuthenticated, )

class GrantViewSet(ModelViewSet):
    queryset = Grant.objects.all()
    serializer_class = GrantSerializer
    permission_classes = (permissions.IsAuthenticated, )

class StandingCommitteViewSet(ModelViewSet):
    queryset = StandingCommittee.objects.all()
    serializer_class = StandingCommitteeSerializer
    permission_classes = (permissions.IsAuthenticated, )

class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = (permissions.IsAuthenticated, )

class CooperativeViewSet(ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    permission_classes = (permissions.IsAuthenticated, )



   
class BorrowerAttachmentViewSet(ModelViewSet):
    queryset = BorrowerAttachment.objects.all()
    serializer_class = BorrowerAttachmentSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = BorrowerAttachment.objects.order_by('id')

        borrowerAttachmentId = self.request.query_params.get('borrowerAttachmentId', None)
        borrowerId = self.request.query_params.get('borrowerId', None)
        

        if borrowerAttachmentId is not None:

           
            queryset = queryset.filter(borrowerAttachment__id=borrowerAttachmentId) 
        
        if borrowerId is not None:

           
            queryset = queryset.filter(borrower=borrowerId) 

        return queryset