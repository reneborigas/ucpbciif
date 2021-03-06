from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()
router.register(r"create-borrower", CreateBorrowerViewSet)
router.register(r"fetch-borrower", FetchBorrowerViewSet)
router.register(r"update-borrower", UpdateBorrowerViewSet)
router.register(r"borrowers", BorrowerViewSet)
router.register(r"borrowerslist", BorrowerListViewSet)
router.register(r"borrowersreports", BorrowerReportViewSet)
router.register(r"business", BusinessViewSet)
router.register(r"individual", IndividualViewSet)

router.register(r"borrowerattachments", BorrowerAttachmentViewSet)
router.register(r"branches", BranchViewSet)

urlpatterns = router.urls