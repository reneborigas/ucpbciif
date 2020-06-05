from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'documents',DocumentViewSet) 
router.register(r'documentmovements',DocumentMovementViewSet) 
urlpatterns = router.urls