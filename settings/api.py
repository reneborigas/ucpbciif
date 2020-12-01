from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import *
from .models import *


class AppNameViewSet(ModelViewSet):
    queryset = AppName.objects.order_by("id")
    serializer_class = AppNameSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = AppName.objects.order_by("id")

        appId = self.request.query_params.get("appId", None)
        appName = self.request.query_params.get("appName", None)

        if appId is not None:
            queryset = queryset.filter(app=appId)

        if appName is not None:
            queryset = queryset.filter(name=appName)

        return queryset


class CooperativeTypeViewSet(ModelViewSet):
    queryset = CooperativeType.objects.order_by("id")
    serializer_class = CooperativeTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TitleTypeViewSet(ModelViewSet):
    queryset = TitleType.objects.order_by("id")
    serializer_class = TitleTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GenderTypeViewSet(ModelViewSet):
    queryset = GenderType.objects.order_by("id")
    serializer_class = GenderTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.order_by("id")
    serializer_class = CountrySerializer
    permission_classes = (permissions.IsAuthenticated,)


class CivilStatusTypeViewSet(ModelViewSet):
    queryset = CivilStatusType.objects.order_by("id")
    serializer_class = CivilStatusTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IdentificationTypeViewSet(ModelViewSet):
    queryset = IdentificationType.objects.order_by("id")
    serializer_class = IdentificationTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IDTypeViewSet(ModelViewSet):
    queryset = IDType.objects.order_by("id")
    serializer_class = IDTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HouseOwnerLesseeTypeViewSet(ModelViewSet):
    queryset = HouseOwnerLesseeType.objects.order_by("id")
    serializer_class = HouseOwnerLesseeTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AddressTypeViewSet(ModelViewSet):
    queryset = AddressType.objects.order_by("id")
    serializer_class = AddressTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ContactTypeViewSet(ModelViewSet):
    queryset = ContactType.objects.order_by("id")
    serializer_class = ContactTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PSICViewSet(ModelViewSet):
    queryset = PSIC.objects.order_by("id")
    serializer_class = PSICSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PSOCViewSet(ModelViewSet):
    queryset = PSOC.objects.order_by("id")
    serializer_class = PSOCSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IncomePeriodViewSet(ModelViewSet):
    queryset = IncomePeriod.objects.order_by("id")
    serializer_class = IncomePeriodSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.order_by("id")
    serializer_class = CurrencySerializer
    permission_classes = (permissions.IsAuthenticated,)


class OccupationStatusTypeViewSet(ModelViewSet):
    queryset = OccupationStatusType.objects.order_by("id")
    serializer_class = OccupationStatusTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class LegalFormTypeViewSet(ModelViewSet):
    queryset = LegalFormType.objects.order_by("id")
    serializer_class = LegalFormTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FirmSizeTypeViewSet(ModelViewSet):
    queryset = FirmSizeType.objects.order_by("id")
    serializer_class = FirmSizeTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ReligionTypeViewSet(ModelViewSet):
    queryset = ReligionType.objects.order_by("id")
    serializer_class = ReligionTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BorrowerDocumentTypeViewSet(ModelViewSet):
    queryset = BorrowerDocumentType.objects.order_by("id")
    serializer_class = BorrowerDocumentTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)
