from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'loans',LoanViewSet) 
router.register(r'terms',TermViewSet)
router.register(r'paymentperiods',PaymentPeriodViewSet) 
urlpatterns = router.urls