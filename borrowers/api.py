from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat


class BorrowerViewSet(ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Borrower.objects.exclude(isDeleted=True).order_by('borrowerId')
        borrowerId = self.request.query_params.get('borrowerId', None)

        if borrowerId is not None:
            queryset = queryset.filter(borrowerId=borrowerId)

        return queryset


class ContactPersonViewSet(ModelViewSet):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
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