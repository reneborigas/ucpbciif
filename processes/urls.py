from rest_framework.routers import DefaultRouter
from .api import *
from django.urls import path

router = DefaultRouter()

router.register(r'subprocesses',SubProcessViewSet) 
router.register(r'steps',StepViewSet) 
router.register(r'outputs',OutputViewSet) 
router.register(r'steprequirements',StepRequirementViewSet) 
router.register(r'steprequirementsattachments',StepRequirementAttachmentViewSet) 
router.register(r'processrequirements',ProcessRequirementViewSet) 
router.register(r'processrequirementsattachments',ProcessRequirementAttachmentViewSet) 
router.register(r'statuses',StatusViewSet) 
 


urlpatterns =  [ path('creditlineapproved/', CreditLineApprovedView.as_view()),
        path('loanavailmentapproved/', LoanAvailmemtApprovedView.as_view()),
        path('loanreleased/', LoanReleasedView.as_view()),
        path('calculatepmt/', CalculatePMTView.as_view()),
        ]


urlpatterns += router.urls
 
