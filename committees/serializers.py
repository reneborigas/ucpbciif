from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *

class CommitteeSerializer(ModelSerializer):
    committeeName = serializers.CharField(read_only=True)
    positionName = serializers.CharField(read_only=True)
    officeName = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        committee = Committee.objects.create(**validated_data) 
        return committee

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get("firstname",instance.firstname)
        instance.middlename = validated_data.get("middlename",instance.middlename)
        instance.lastname = validated_data.get("lastname",instance.lastname)
        instance.address = validated_data.get("address",instance.address)
        instance.telNo = validated_data.get("telNo",instance.telNo)
        instance.emailAddress = validated_data.get("emailAddress",instance.emailAddress)
        instance.phoneNo = validated_data.get("phoneNo",instance.phoneNo)
        instance.user = validated_data.get("user",instance.user)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)

        instance.save()

        return instance
    
    class Meta:
        model = Committee          
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    committeeName = serializers.CharField(read_only=True)
    positionName = serializers.ReadOnlyField(source='committee.position.name')
    def create(self, validated_data):
        note = Note.objects.create(**validated_data) 
        return note

    def update(self, instance, validated_data):
        instance.save()
        return instance
    
    class Meta:
        model = Note          
        fields = '__all__'

class PositionSerializer(ModelSerializer):
    committees = CommitteeSerializer(many=True,required=False)
    def create(self, validated_data):
        position = Position.objects.create(**validated_data) 
        return position

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.description = validated_data.get("description",instance.description)
        instance.remarks = validated_data.get("remarks",instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
        instance.save()

        return instance
    
    class Meta:
        model = Position          
        fields = '__all__'    

class OfficeSerializer(ModelSerializer):

    def create(self, validated_data):
        office = Office.objects.create(**validated_data)

        return office

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.description = validated_data.get("description",instance.description)
        instance.remarks = validated_data.get("remarks",instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
        instance.save()

        return instance

    class Meta:
        model = Office          
        fields = '__all__'   