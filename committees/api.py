from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat


class OfficeViewSet(ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Office.objects.exclude(isDeleted=True)

        officeName = self.request.query_params.get('officeName', None)
      
        if officeName is not None:
            queryset = queryset.filter(name__icontains=officeName)

        return queryset

class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Position.objects.exclude(isDeleted=True)

        positionId = self.request.query_params.get('positionId', None)
        officeId = self.request.query_params.get('officeId', None)
      
        if positionId is not None:
            queryset = queryset.filter(id=positionId)

        if officeId is not None:
            queryset = queryset.filter(office=officeId)

        return queryset

class CommitteeViewSet(ModelViewSet):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Committee.objects.exclude(isDeleted=True).order_by('-id')
       
        committeeId = self.request.query_params.get('committeeId', None)
        positionId = self.request.query_params.get('positionId', None)
      
        if committeeId is not None:
            queryset = queryset.filter(id=committeeId)

        if positionId is not None:
            queryset = queryset.filter(position=positionId)

        return queryset


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Note.objects.annotate(
            committeeName=Concat(F('committee__firstname'),V(' '),F('committee__middlename'),V(' '),F('committee__lastname'))
        ).exclude(isDeleted=True).order_by('id')

        noteId = self.request.query_params.get('noteId', None)
        content_type = self.request.query_params.get('content_type', None)
        object_id = self.request.query_params.get('object_id', None)
        
        if object_id is not None and content_type is not None:
            queryset = queryset.filter(content_type=content_type,object_id=object_id) 
            
        if noteId is not None:
            queryset = queryset.filter(id=noteId) 

        return queryset
