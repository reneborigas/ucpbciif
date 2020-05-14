from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'loans',LoanViewSet) 
urlpatterns = router.urls