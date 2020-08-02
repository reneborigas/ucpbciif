from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, parsers
from .serializers import *
from .models import *
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum, ExpressionWrapper,OuterRef, Subquery, Func
from django.db.models.functions import Coalesce, Cast, TruncDate, Concat
 
from committees.models import Committee
 
from rest_framework import status, views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from users.models import CustomUser

class ViewNotification(views.APIView):
    
    # @method_decorator(csrf_protect) 
    def post(self,request): 

        notificationId = request.data.get("notificationId") 
        committeeId = request.data.get("committeeId") 
        userId = request.data.get("userId") 
        
        # subProcessId = request.data.get("subProcessId") 
        
        if notificationId and committeeId:  
          
            notificationView = NotificationView(notification=Notification.objects.get(pk=notificationId),committee=Committee.objects.get(pk=committeeId))
            
            notificationView.save()

        if notificationId and userId:  
          
            notificationView = NotificationView(notification=Notification.objects.get(pk=notificationId),user=CustomUser.objects.get(pk=userId))
            
            notificationView.save()


            return Response({
                'message': 'Notification Viewed', 
                'notification': notificationView.id 
            },status= status.HTTP_202_ACCEPTED) 


        return Response({'error':'Error on viewing notification'},status.HTTP_400_BAD_REQUEST)
        
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NoteSerializer 
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self): 
        queryset = Notification.objects.annotate(
            committeeName=Concat(F('committee__firstname'),V(' '),F('committee__middlename'),V(' '),F('committee__lastname'))
        ).exclude(isDeleted=True).order_by('-id')

        committeeId = self.request.query_params.get('committeeId', None)
        userId = self.request.query_params.get('userId', None)
        content_type = self.request.query_params.get('content_type', None)
        object_id = self.request.query_params.get('object_id', None)
        

        
        if object_id is not None and content_type is not None:
            queryset = queryset.filter(content_type=content_type,object_id=object_id) 
            
        if committeeId is not None: 
            notificationViews = NotificationView.objects.filter(committee__id=committeeId)
            
            notifications = []

            for notificationview in notificationViews:
                notifications.append(notificationview.notification.id)


                queryset = queryset.exclude(id__in=notifications) 
            
        if userId is not None: 
            notificationViews = NotificationView.objects.filter(user__id=userId)

            notifications = []

            for notificationview in notificationViews:
                notifications.append(notificationview.notification.id)


                queryset = queryset.exclude(id__in=notifications) 
          
        return queryset
