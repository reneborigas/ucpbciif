from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'subprocesses',SubProcessViewSet) 
router.register(r'steps',StepViewSet) 
router.register(r'outputs',OutputViewSet) 
router.register(r'steprequirements',StepRequirementViewSet) 
router.register(r'steprequirementsattachments',StepRequirementAttachmentViewSet) 

urlpatterns = router.urls