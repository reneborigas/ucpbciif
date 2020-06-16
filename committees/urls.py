from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'committees',CommitteeViewSet) 
router.register(r'notes',NoteViewSet) 
urlpatterns = router.urls