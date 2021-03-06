from rest_framework.routers import DefaultRouter
from .api import *
from django.urls import path


router = DefaultRouter()

router.register(r"documents", DocumentViewSet)
router.register(r"documentslist", DocumentListViewSet)

router.register(r"documentsloanapplicationreport", DocumentLoanApplicationReportViewSet)

router.register(r"documentmovements", DocumentMovementViewSet)

urlpatterns = [
    path("getdocumentfilename/", GetDocumentFileName.as_view()),
]


urlpatterns += router.urls
