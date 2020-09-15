from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from settings.models import AppName
from django.db.models import Q, Prefetch,F,Value as V, Count, Sum, Max, Case, When



class UserAppsViewSet(ModelViewSet):
    queryset = UserApps.objects.all()
    serializer_class = UserAppsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = UserApps.objects.prefetch_related(
            Prefetch('installedApps',queryset=AppName.objects.order_by('id'))
        ).all()

        user = self.request.query_params.get('user', None)
        
        if user is not None:
            queryset = queryset.filter(user=user)

        return queryset

class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    # parser_classes = (parsers.MultiPartParser, parsers.FormParser,)

    # def perform_create(self, serializer):
    #     serializer.save(profile_picture=self.request.data.get('profile_picture'))

    def pre_save(self, obj):
        obj.profile_picture = self.request.FILES.get('file')

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = CustomUser.objects.prefetch_related(
            Prefetch('appAccess',UserApps.objects.all())
        ).annotate(
            fullName=F('profile__name'),
            account_type_text=F('account_type__account_type'),
            committeePosition=F('committees__position__name'),
            committeeId=F('committees__id'),
            positionId=F('committees__position__id'),
        ).exclude(is_active=False)
        id = self.request.query_params.get('id', None)
        
        if id is not None:
            queryset = queryset.filter(id=id).exclude(is_active=False)
        return queryset

class UserLogsViewSet(ModelViewSet):
    queryset = UserLogs.objects.all()
    serializer_class = UserLogsSerializer

    def get_queryset(self):
        var1 = 'content_type__model'
        queryset = UserLogs.objects.annotate(
            userName=F('user__profile__name'),
        ).order_by('-id')
        content_type = self.request.query_params.get('content_type', None)
        object_id = self.request.query_params.get('object_id', None)
        user = self.request.query_params.get('user', None)

        if content_type is not None:
            queryset = queryset.filter(content_type=content_type,object_id=object_id)

        if user is not None:
            queryset = queryset.filter(user=user)

        return queryset

class ContentTypeViewSet(ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer

    def get_queryset(self):
        queryset = ContentType.objects.all()
        model = self.request.query_params.get('model', None)
        
        if model is not None:
            queryset = queryset.filter(model=model)

        return queryset

class AccountTypeViewSet(ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

    def get_queryset(self):
        queryset = AccountType.objects.all()
        account_type = self.request.query_params.get('account_type', None)
        
        if account_type is not None:
            queryset = queryset.filter(account_type=account_type)

        return queryset

