from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class AppNameSerializer(ModelSerializer):
    class Meta:
        model = AppName
        fields = '__all__'

class CooperativeTypeSerializer(ModelSerializer):
    class Meta:
        model = CooperativeType
        fields = '__all__'

class TitleTypeSerializer(ModelSerializer):
    class Meta:
        model = TitleType
        fields = '__all__'

class GenderTypeSerializer(ModelSerializer):
    class Meta:
        model = GenderType
        fields = '__all__'

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CivilStatusTypeSerializer(ModelSerializer):
    class Meta:
        model = CivilStatusType
        fields = '__all__'

class IdentificationTypeSerializer(ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = '__all__'

class IDTypeSerializer(ModelSerializer):
    class Meta:
        model = IDType
        fields = '__all__'

class HouseOwnerLesseeTypeSerializer(ModelSerializer):
    class Meta:
        model = HouseOwnerLesseeType
        fields = '__all__'

class AddressTypeSerializer(ModelSerializer):
    class Meta:
        model = AddressType
        fields = '__all__'

class ContactTypeSerializer(ModelSerializer):
    class Meta:
        model = ContactType
        fields = '__all__'

class PSICSerializer(ModelSerializer):
    class Meta:
        model = PSIC
        fields = '__all__'

class PSOCSerializer(ModelSerializer):
    class Meta:
        model = PSOC
        fields = '__all__'

class IncomePeriodSerializer(ModelSerializer):
    class Meta:
        model = IncomePeriod
        fields = '__all__'

class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class OccupationStatusTypeSerializer(ModelSerializer):
    class Meta:
        model = OccupationStatusType
        fields = '__all__'

class LegalFormTypeSerializer(ModelSerializer):
    class Meta:
        model = LegalFormType
        fields = '__all__'

class FirmSizeTypeSerializer(ModelSerializer):
    class Meta:
        model = FirmSizeType
        fields = '__all__'