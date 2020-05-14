from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import *
from .models import *

class GenderTypeViewSet(ModelViewSet):
    queryset = GenderType.objects.exclude(isDeleted=True).order_by('id')
    serializer_class = GenderTypeSerializer
    # permission_classes = (permissions.IsAuthenticated, )

class CooperativeTypeViewSet(ModelViewSet):
    queryset = CooperativeType.objects.exclude(isDeleted=True).order_by('id')
    serializer_class = CooperativeTypeSerializer
    # permission_classes = (permissions.IsAuthenticated, )