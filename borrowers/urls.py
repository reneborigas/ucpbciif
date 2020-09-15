from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'crud-borrowers',CRUDBorrowerViewSet)
router.register(r'borrowers',BorrowerViewSet)
router.register(r'business',BusinessViewSet)
router.register(r'borrowerattachments',BorrowerAttachmentViewSet)

urlpatterns = router.urls