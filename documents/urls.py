from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'documents',DocumentViewSet) 
urlpatterns = router.urls