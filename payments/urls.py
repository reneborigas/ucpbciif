from rest_framework.routers import DefaultRouter
from .api import *
from django.urls import path
router = DefaultRouter()

router.register(r'checks',CheckViewSet) 
router.register(r'checkstatuses',CheckStatusViewSet) 
router.register(r'paymentstatus',PaymentStatusViewSet) 
router.register(r'paymenttypes',PaymentTypeViewSet)
router.register(r'payments',PaymentViewSet) 


urlpatterns = [
    path("skippayment/", SkipPaymentView.as_view()), 
]

urlpatterns += router.urls