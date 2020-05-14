from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()
router.register(r'gendertype',GenderTypeViewSet)
urlpatterns = router.urls