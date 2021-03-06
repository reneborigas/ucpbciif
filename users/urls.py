from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()
router.register(r'userapps',UserAppsViewSet)
router.register(r'userprofile',ProfileViewSet)
router.register(r'users',UserViewSet)
router.register(r'userlogs',UserLogsViewSet)
router.register(r'contenttype',ContentTypeViewSet)
router.register(r'accounttype',AccountTypeViewSet)

urlpatterns = router.urls 