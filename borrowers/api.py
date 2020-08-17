from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
from documents.models import Document,DocumentMovement
from loans.models import Loan
from payments.models import Payment



class CRUDBorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = CRUDBorrowerSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Borrower.objects.annotate(
            contactPersonName=Concat(F('contactPerson__firstname'),V(' '),F('contactPerson__middlename'),V(' '),F('contactPerson__lastname')),
            cooperativeName=F('cooperative__name'),
            tin=F('cooperative__tin'),
            address=F('cooperative__address'),
            phoneNo=F('cooperative__phoneNo'),
        ).exclude(isDeleted=True).order_by('borrowerId')
        borrowerId = self.request.query_params.get('borrowerId', None)

        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        return queryset

class BorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Borrower.objects.prefetch_related('borrowerAttachments',  Prefetch( 'documents',queryset=Document.objects.order_by('dateCreated')),
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
        totalAvailmentsFrom = self.request.query_params.get('totalAvailmentsFrom', None)
        totalAvailmentsTo = self.request.query_params.get('totalAvailmentsTo', None)
        totalOutstandingBalanceFrom = self.request.query_params.get('totalOutstandingBalanceFrom', None)
        totalOutstandingBalanceTo = self.request.query_params.get('totalOutstandingBalanceTo', None)
        totalPaymentsFrom = self.request.query_params.get('totalPaymentsFrom', None)
        totalPaymentsTo = self.request.query_params.get('totalPaymentsTo', None)

        clientSinceFrom = self.request.query_params.get('clientSinceFrom', None)
        clientSinceTo = self.request.query_params.get('clientSinceTo', None)


# .filter(status__name='RELEASED')
        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        
        if totalAvailmentsFrom is not None and totalAvailmentsTo is not None:
            borrowers = []
            for borrower in queryset: 
                borrower.totalAvailments = borrower.getTotalAvailments()
                if (int(borrower.totalAvailments) >= int(totalAvailmentsFrom)) and  (int(borrower.totalAvailments) <= int(totalAvailmentsTo)):
                    borrowers.append(borrower.pk)

            queryset=queryset.filter(borrowerId__in=borrowers)

        if totalOutstandingBalanceFrom is not None and totalOutstandingBalanceTo is not None:
            borrowers = []
            for borrower in queryset: 
                borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance()
                if (int(borrower.totalOutstandingBalance) >= int(totalOutstandingBalanceFrom)) and  (int(borrower.totalOutstandingBalance) <= int(totalOutstandingBalanceTo)):
                    borrowers.append(borrower.pk)
                    
            queryset=queryset.filter(borrowerId__in=borrowers)
        
        if totalPaymentsFrom is not None and totalPaymentsTo is not None:
            borrowers = []
            for borrower in queryset: 
                borrower.payments = borrower.getPayments()
                borrower.totalPayments = borrower.getTotalPayments()
                if (int(borrower.totalPayments) >= int(totalPaymentsFrom)) and  (int(borrower.totalPayments) <= int(totalPaymentsTo)):
                    borrowers.append(borrower.pk)
                    
            queryset=queryset.filter(borrowerId__in=borrowers)

        if clientSinceFrom is not None and clientSinceTo is not None:
            queryset=queryset.filter(clientSince__gte=clientSinceFrom).filter(clientSince__lte=clientSinceTo)
        
        for borrower in queryset:
            borrower.totalAvailments = borrower.getTotalAvailments()
            borrower.totalOutstandingBalance = borrower.getTotalOutstandingBalance()

            

            borrower.payments = borrower.getPayments()
            borrower.totalPayments = borrower.getTotalPayments()

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