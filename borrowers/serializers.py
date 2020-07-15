from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from documents.serializers import DocumentSerializer
from processes.serializers import SubProcessSerializer
from loans.serializers import LoanSerializer
class ContactPersonSerializer(ModelSerializer):
    contactPersonName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        contactPerson = ContactPerson.objects.create(**validated_data)

        return contactPerson

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.middlename = validated_data.get("middlename", instance.middlename)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.address = validated_data.get("address", instance.address)
        instance.telNo = validated_data.get("telNo", instance.telNo)
        instance.emailAddress = validated_data.get("emailAddress", instance.emailAddress)
        instance.phoneNo = validated_data.get("phoneNo", instance.phoneNo)
        instance.dateUpdated = validated_data.get("dateUpdated", instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted", instance.isDeleted)
        instance.save()

        return instance
    
    class Meta:
        model = ContactPerson        
        fields = '__all__'

class GrantSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Grant
        fields = '__all__'
        read_only_fields = ('cooperative', )

class StandingCommitteeSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = StandingCommittee
        fields = '__all__'
        read_only_fields = ('cooperative', )

class DirectorSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Director
        fields = '__all__'
        read_only_fields = ('cooperative', )


class CooperativeSerializer(ModelSerializer):
    directors = DirectorSerializer(many=True,required=False)
    standingCommittees = StandingCommitteeSerializer(many=True,required=False)
    grants = GrantSerializer(many=True,required=False)
    cooperativeTypeText = serializers.CharField(read_only=True)

    def create(self, validated_data):
        directors = validated_data.pop('directors')
        standingCommittees = validated_data.pop('standingCommittees')
        grants = validated_data.pop('grants')

        cooperative = Cooperative.objects.create(**validated_data)

        for director in directors:
            Director.objects.create(**director,cooperative=cooperative)

        for standingCommittee in standingCommittees:
            StandingCommittee.objects.create(**standingCommittee,cooperative=cooperative)
        
        for grant in grants:
            Grant.objects.create(**grant,cooperative=cooperative)

        return cooperative

    def update(self, instance, validated_data):
        directors = validated_data.get('directors')
        standingCommittees = validated_data.get('standingCommittees')
        grants = validated_data.get('grants')

        instance.name = validated_data.get("name",instance.name)
        instance.icRiskRating = validated_data.get("icRiskRating",instance.icRiskRating)
        instance.tin = validated_data.get("tin",instance.tin)
        instance.cdaRegistrationDate = validated_data.get("cdaRegistrationDate",instance.cdaRegistrationDate)
        instance.initialMembershipSize = validated_data.get("initialMembershipSize",instance.initialMembershipSize)
        instance.membershipSize = validated_data.get("membershipSize",instance.membershipSize)
        instance.paidUpCapitalInitial = validated_data.get("paidUpCapitalInitial",instance.paidUpCapitalInitial)
        instance.noOfCooperators = validated_data.get("noOfCooperators",instance.noOfCooperators)
        instance.coconutFarmers = validated_data.get("coconutFarmers",instance.coconutFarmers)
        instance.authorized = validated_data.get("authorized",instance.authorized)
        instance.fullyPaidSharesNo = validated_data.get("fullyPaidSharesNo",instance.fullyPaidSharesNo)
        instance.bookValue = validated_data.get("bookValue",instance.bookValue)
        instance.parValue = validated_data.get("parValue",instance.parValue)
        instance.paidUp = validated_data.get("paidUp",instance.paidUp)
        instance.fullyPaidPercent = validated_data.get("fullyPaidPercent",instance.fullyPaidPercent)
        instance.initialPaidUpShare = validated_data.get("initialPaidUpShare",instance.initialPaidUpShare)
        instance.address = validated_data.get("address",instance.address)
        instance.telNo = validated_data.get("telNo",instance.telNo)
        instance.emailAddress = validated_data.get("emailAddress",instance.emailAddress)
        instance.phoneNo = validated_data.get("phoneNo",instance.phoneNo)
        instance.fax = validated_data.get("fax",instance.fax)
        instance.cooperativeType = validated_data.get("cooperativeType",instance.cooperativeType)
        instance.description = validated_data.get("description",instance.description)
        instance.remarks = validated_data.get("remarks",instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
        instance.save()

        keep_directors = []        
        if directors:
            for director in directors:
                if 'id' in director.keys():
                    if Director.objects.filter(id=director['id']).exists():   
                        e = Director.objects.get(id=director['id'])
                        e.name = director.get('name',e.name)
                        e.position = director.get('position',e.position)
                        e.educationalAttainment = director.get('educationalAttainment',e.educationalAttainment)
                        e.age = director.get('age',e.age)
                        e.yearsInCoop = director.get('yearsInCoop',e.yearsInCoop)
                        e.oSLoanWithCoop = director.get('oSLoanWithCoop',e.oSLoanWithCoop)
                        e.status = director.get('status',e.status)
                        e.dateUpdated = director.get('dateUpdated',e.dateUpdated)
                        e.isDeleted = director.get('isDeleted',e.isDeleted)
                        e.save()
                        keep_directors.append(e.id)
                    else:
                        continue
                else:
                    e = Director.objects.create(**director, cooperative=instance)
                    keep_directors.append(e.id)

            for director in instance.directors.all():
                if director.id not in keep_directors:
                    directors.delete()

        keep_standingCommittees = []        
        if standingCommittees:
            for standingCommittee in standingCommittees:
                if 'id' in standingCommittee.keys():
                    if StandingCommittee.objects.filter(id=standingCommittee['id']).exists():   
                        e = StandingCommittee.objects.get(id=standingCommittee['id'])
                        e.name = standingCommittee.get('name',e.name)
                        e.department = standingCommittee.get('department',e.department)
                        e.position = standingCommittee.get('position',e.position)
                        e.educationalAttainment = standingCommittee.get('educationalAttainment',e.educationalAttainment)
                        e.age = standingCommittee.get('age',e.age)
                        e.yearsInCoop = standingCommittee.get('yearsInCoop',e.yearsInCoop)
                        e.oSLoanWithCoop = standingCommittee.get('oSLoanWithCoop',e.oSLoanWithCoop)
                        e.status = standingCommittee.get('status',e.status)
                        e.dateUpdated = standingCommittee.get('dateUpdated',e.dateUpdated)
                        e.isDeleted = standingCommittee.get('isDeleted',e.isDeleted)
                        e.save()
                        keep_standingCommittees.append(e.id)
                    else:
                        continue
                else:
                    e = StandingCommittee.objects.create(**standingCommittee, cooperative=instance)
                    keep_standingCommittees.append(e.id)

            for standingCommittee in instance.standingCommittees.all():
                if standingCommittee.id not in keep_standingCommittees:
                    standingCommittees.delete()

        keep_grants = []        
        if grants:
            for grant in grants:
                if 'id' in grant.keys():
                    if Grant.objects.filter(id=grant['id']).exists():   
                        e = Grant.objects.get(id=grant['id'])
                        e.donor = grant.get('donor',e.donor)
                        e.projectType = grant.get('projectType',e.projectType)
                        e.amount = grant.get('amount',e.amount)
                        e.projectStatus = grant.get('projectStatus',e.projectStatus)
                        e.dateUpdated = grant.get('dateUpdated',e.dateUpdated)
                        e.isDeleted = grant.get('isDeleted',e.isDeleted)
                        e.save()
                        keep_grants.append(e.id)
                    else:
                        continue
                else:
                    e = Grant.objects.create(**grant, cooperative=instance)
                    keep_grants.append(e.id)

            for grant in instance.grants.all():
                if grant.id not in keep_grants:
                    grants.delete()

        return instance
    
    class Meta:
        model = Cooperative        
        fields = '__all__'



class BorrowerAttachmentSerializer(ModelSerializer):

    def create(self, validated_data):
        borrowerAttachment = BorrowerAttachment.objects.create(**validated_data) 
        
        return borrowerAttachment

    def update(self, instance, validated_data):
        instance.save()

        return instance
    
    class Meta:
        model = BorrowerAttachment          
        fields = '__all__'  
class BorrowerSerializer(ModelSerializer):
    contactPersonName = serializers.CharField(read_only=True)
    cooperativeName = serializers.CharField(read_only=True)
    tin = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phoneNo = serializers.CharField(read_only=True)
    contactPerson = ContactPersonSerializer()
    cooperative = CooperativeSerializer()
    documents = DocumentSerializer(many=True)
     
    borrowerAttachments = BorrowerAttachmentSerializer(many=True)
    totalAvailments = serializers.CharField(read_only=True)
    totalAvailmentPerProgram = serializers.CharField(read_only=True)
    totalOutstandingBalance = serializers.CharField(read_only=True)
    loans = LoanSerializer(many=True,read_only=True)
    def create(self, validated_data):
        borrower = Borrower.objects.create(**validated_data)
    
        return borrower


    def createLoanApplication(self, validated_data):
        borrower = Borrower.objects.create(**validated_data)
    
        return borrower
    def update(self, instance, validated_data):

        print("here")
        print(validated_data)
        instance.status = validated_data.get("status",instance.status)
        instance.clientSince = validated_data.get("clientSince",instance.clientSince)
        instance.remarks = validated_data.get("remarks",instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
        instance.save()

        return instance
    
    class Meta:
        model = Borrower        
        fields = '__all__'
