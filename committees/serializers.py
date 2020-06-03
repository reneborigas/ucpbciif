from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *


class CommitteeSerializer(ModelSerializer):
    committeeName = serializers.CharField(read_only=True)
    def create(self, validated_data):
        committee = Committee.objects.create(**validated_data) 
        return committee

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Committee          
        fields = '__all__'