from rest_framework.routers import DefaultRouter
from .api import *
from django.urls import path


router = DefaultRouter()

router.register(r'notifications',NotificationViewSet)  
 



urlpatterns =  [ 
        path('viewnotifications/', ViewNotification.as_view()), 
        path('clearnotifications/', ClearNotification.as_view()), 
        ]

urlpatterns += router.urls

