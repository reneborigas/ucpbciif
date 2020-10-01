from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()
router.register(r'chartofaccountstype',ChartOfAccountTypeViewSet)
router.register(r'chartofaccounts',ChartOfAccountViewSet)
urlpatterns = router.urls