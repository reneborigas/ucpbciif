from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'crud-borrowers',CRUDBorrowerViewSet)
router.register(r'borrowers',BorrowerViewSet)
router.register(r'contactpersons',ContactPersonViewSet)
router.register(r'grants',GrantViewSet)
router.register(r'standingcommittees',StandingCommitteViewSet)
router.register(r'directors',DirectorViewSet)
router.register(r'cooperatives',CooperativeViewSet)
router.register(r'borrowerattachments',BorrowerAttachmentViewSet)


urlpatterns = router.urls