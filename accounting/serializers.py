from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *

class ChartOfAccountSerializer(ModelSerializer):
    createdByName = serializers.CharField(read_only=True,required=False)
    accountTypeText = serializers.CharField(read_only=True,required=False)
    groupText = serializers.CharField(read_only=True,required=False)
    accountSide = serializers.CharField(read_only=True,required=False)
    
    class Meta:
        model = ChartOfAccount
        fields = '__all__'

class ChartOfAccountTypeSerializer(ModelSerializer):
    chartOfAccounts = ChartOfAccountSerializer(many=True,required=False)
    class Meta:
        model = ChartOfAccountType
        fields = '__all__'