from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'crud-borrowers',CRUDBorrowerViewSet)
router.register(r'borrowers',BorrowerViewSet)
router.register(r'borrowersreports',BorrowerReportViewSet)
router.register(r'business',BusinessViewSet)
router.register(r'borrowerattachments',BorrowerAttachmentViewSet)
router.register(r'branches',BranchViewSet)

urlpatterns = router.urls