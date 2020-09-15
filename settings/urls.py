from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r'appname',AppNameViewSet)
router.register(r'cooperativetype',CooperativeTypeViewSet)
router.register(r'titletype',TitleTypeViewSet)
router.register(r'gendertype',GenderTypeViewSet)
router.register(r'countries',CountryViewSet)
router.register(r'civilstatustype',CivilStatusTypeViewSet)
router.register(r'identificationtype',IdentificationTypeViewSet)
router.register(r'idtype',IDTypeViewSet)
router.register(r'houseownerlessee',HouseOwnerLesseeTypeViewSet)
router.register(r'addresstype',AddressTypeViewSet)
router.register(r'contacttype',ContactTypeViewSet)
router.register(r'psic',PSICViewSet)
router.register(r'psoc',PSOCViewSet)
router.register(r'incomeperiod',IncomePeriodViewSet)
router.register(r'currencies',CurrencyViewSet)
router.register(r'occupationstatustype',OccupationStatusTypeViewSet)
router.register(r'legalformtype',LegalFormTypeViewSet)
router.register(r'firmsizetype',FirmSizeTypeViewSet)

urlpatterns = router.urls