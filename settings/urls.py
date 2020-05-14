from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()
router.register(r'gendertype',GenderTypeViewSet)
router.register(r'cooperativetype',CooperativeTypeViewSet)
urlpatterns = router.urls