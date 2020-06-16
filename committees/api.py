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


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Note.objects.exclude(isDeleted=True).order_by('id')
       

        noteId = self.request.query_params.get('noteId', None)
        content_type = self.request.query_params.get('content_type', None)
        
        object_id = self.request.query_params.get('object_id', None)
        
        if object_id is not None and content_type is not None :
            
            queryset = queryset.filter(content_type=content_type,object_id=object_id) 
            
        if noteId is not None:
            queryset = queryset.filter(id=noteId) 
 

        return queryset
