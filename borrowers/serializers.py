from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from documents.serializers import DocumentSerializer
from processes.serializers import SubProcessSerializer
from loans.serializers import LoanSerializer,CreditLineSerializer
from payments.serializers import PaymentSerializer

class FamilySerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Family
        fields = '__all__'
        read_only_fields = ('individual', )

class AddressSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('individual','business', )

class IdentificationSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Identification
        fields = '__all__'
        read_only_fields = ('individual','business', )

class IDSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ID
        fields = '__all__'
        read_only_fields = ('individual', )

class ContactSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('individual','business' )

class EmploymentSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Employment
        fields = '__all__'
        read_only_fields = ('individual', )

class SoleTraderSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SoleTrader
        fields = '__all__'
        read_only_fields = ('individual', )


class ContactPersonSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ContactPerson        
        fields = '__all__'
        read_only_fields = ('business', )

class BackgroundSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Background
        fields = '__all__'
        read_only_fields = ('business', )

class DirectorSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Director
        fields = '__all__'
        read_only_fields = ('business', )

class StandingCommitteeSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = StandingCommittee
        fields = '__all__'
        read_only_fields = ('business', )

class GrantSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Grant
        fields = '__all__'
        read_only_fields = ('business', )


class BusinessSerializer(ModelSerializer):
    businessAddress = AddressSerializer(many=True,required=False)
    businessIdentification = IdentificationSerializer(many=True,required=False)
    businessContact = ContactSerializer(many=True,required=False)
    businessContactPerson = ContactPersonSerializer(many=True,required=False)
    businessBackground = BackgroundSerializer(many=True,required=False)
    businessDirectors = DirectorSerializer(many=True,required=False)
    businessStandingCommittees = StandingCommitteeSerializer(many=True,required=False)
    businessGrants = GrantSerializer(many=True,required=False)

    def create(self, validated_data):
        businessAddress = validated_data.pop('businessAddress')
        businessIdentification = validated_data.pop('businessIdentification')
        businessContact = validated_data.pop('businessContact')
        businessContactPerson = validated_data.pop('businessContactPerson')
        businessBackground = validated_data.pop('businessBackground')
        businessDirectors = validated_data.pop('businessDirectors')
        businessStandingCommittees = validated_data.pop('businessStandingCommittees')
        businessGrants = validated_data.pop('businessGrants')

        business = Business.objects.create(**validated_data)

        for address in businessAddress:
            Address.objects.create(**address,business=business)

        for identification in businessIdentification:
            Identification.objects.create(**identification,business=business)

        for contact in businessContact:
            Contact.objects.create(**contact,business=business)

        for contactPerson in businessContactPerson:
            ContactPerson.objects.create(**contactPerson,business=business)
    
        for background in businessBackground:
            Background.objects.create(**background,business=business)

        for directors in businessDirectors:
            Director.objects.create(**directors,business=business)

        for standingCommittee in businessStandingCommittees:
            StandingCommittee.objects.create(**standingCommittee,business=business)

        for grants in businessGrants:
            Grant.objects.create(**grants,business=business)

        return business

    # def update(self, instance, validated_data):
    #     directors = validated_data.get('directors')
    #     standingCommittees = validated_data.get('standingCommittees')
    #     grants = validated_data.get('grants')

    #     instance.name = validated_data.get("name",instance.name)
    #     instance.icRiskRating = validated_data.get("icRiskRating",instance.icRiskRating)
    #     instance.tin = validated_data.get("tin",instance.tin)
    #     instance.cdaRegistrationDate = validated_data.get("cdaRegistrationDate",instance.cdaRegistrationDate)
    #     instance.initialMembershipSize = validated_data.get("initialMembershipSize",instance.initialMembershipSize)
    #     instance.membershipSize = validated_data.get("membershipSize",instance.membershipSize)
    #     instance.paidUpCapitalInitial = validated_data.get("paidUpCapitalInitial",instance.paidUpCapitalInitial)
    #     instance.noOfCooperators = validated_data.get("noOfCooperators",instance.noOfCooperators)
    #     instance.coconutFarmers = validated_data.get("coconutFarmers",instance.coconutFarmers)
    #     instance.authorized = validated_data.get("authorized",instance.authorized)
    #     instance.fullyPaidSharesNo = validated_data.get("fullyPaidSharesNo",instance.fullyPaidSharesNo)
    #     instance.bookValue = validated_data.get("bookValue",instance.bookValue)
    #     instance.parValue = validated_data.get("parValue",instance.parValue)
    #     instance.paidUp = validated_data.get("paidUp",instance.paidUp)
    #     instance.fullyPaidPercent = validated_data.get("fullyPaidPercent",instance.fullyPaidPercent)
    #     instance.initialPaidUpShare = validated_data.get("initialPaidUpShare",instance.initialPaidUpShare)
    #     instance.address = validated_data.get("address",instance.address)
    #     instance.telNo = validated_data.get("telNo",instance.telNo)
    #     instance.emailAddress = validated_data.get("emailAddress",instance.emailAddress)
    #     instance.phoneNo = validated_data.get("phoneNo",instance.phoneNo)
    #     instance.fax = validated_data.get("fax",instance.fax)
    #     instance.cooperativeType = validated_data.get("cooperativeType",instance.cooperativeType)
    #     instance.description = validated_data.get("description",instance.description)
    #     instance.remarks = validated_data.get("remarks",instance.remarks)
    #     instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
    #     instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
    #     instance.save()

    #     keep_directors = []        
    #     if directors:
    #         for director in directors:
    #             if 'id' in director.keys():
    #                 if Director.objects.filter(id=director['id']).exists():   
    #                     e = Director.objects.get(id=director['id'])
    #                     e.name = director.get('name',e.name)
    #                     e.position = director.get('position',e.position)
    #                     e.educationalAttainment = director.get('educationalAttainment',e.educationalAttainment)
    #                     e.age = director.get('age',e.age)
    #                     e.yearsInCoop = director.get('yearsInCoop',e.yearsInCoop)
    #                     e.oSLoanWithCoop = director.get('oSLoanWithCoop',e.oSLoanWithCoop)
    #                     e.status = director.get('status',e.status)
    #                     e.dateUpdated = director.get('dateUpdated',e.dateUpdated)
    #                     e.isDeleted = director.get('isDeleted',e.isDeleted)
    #                     e.save()
    #                     keep_directors.append(e.id)
    #                 else:
    #                     continue
    #             else:
    #                 e = Director.objects.create(**director, cooperative=instance)
    #                 keep_directors.append(e.id)

    #         for director in instance.directors.all():
    #             if director.id not in keep_directors:
    #                 directors.delete()

    #     keep_standingCommittees = []        
    #     if standingCommittees:
    #         for standingCommittee in standingCommittees:
    #             if 'id' in standingCommittee.keys():
    #                 if StandingCommittee.objects.filter(id=standingCommittee['id']).exists():   
    #                     e = StandingCommittee.objects.get(id=standingCommittee['id'])
    #                     e.name = standingCommittee.get('name',e.name)
    #                     e.department = standingCommittee.get('department',e.department)
    #                     e.position = standingCommittee.get('position',e.position)
    #                     e.educationalAttainment = standingCommittee.get('educationalAttainment',e.educationalAttainment)
    #                     e.age = standingCommittee.get('age',e.age)
    #                     e.yearsInCoop = standingCommittee.get('yearsInCoop',e.yearsInCoop)
    #                     e.oSLoanWithCoop = standingCommittee.get('oSLoanWithCoop',e.oSLoanWithCoop)
    #                     e.status = standingCommittee.get('status',e.status)
    #                     e.dateUpdated = standingCommittee.get('dateUpdated',e.dateUpdated)
    #                     e.isDeleted = standingCommittee.get('isDeleted',e.isDeleted)
    #                     e.save()
    #                     keep_standingCommittees.append(e.id)
    #                 else:
    #                     continue
    #             else:
    #                 e = StandingCommittee.objects.create(**standingCommittee, cooperative=instance)
    #                 keep_standingCommittees.append(e.id)

    #         for standingCommittee in instance.standingCommittees.all():
    #             if standingCommittee.id not in keep_standingCommittees:
    #                 standingCommittees.delete()

    #     keep_grants = []        
    #     if grants:
    #         for grant in grants:
    #             if 'id' in grant.keys():
    #                 if Grant.objects.filter(id=grant['id']).exists():   
    #                     e = Grant.objects.get(id=grant['id'])
    #                     e.donor = grant.get('donor',e.donor)
    #                     e.projectType = grant.get('projectType',e.projectType)
    #                     e.amount = grant.get('amount',e.amount)
    #                     e.projectStatus = grant.get('projectStatus',e.projectStatus)
    #                     e.dateUpdated = grant.get('dateUpdated',e.dateUpdated)
    #                     e.isDeleted = grant.get('isDeleted',e.isDeleted)
    #                     e.save()
    #                     keep_grants.append(e.id)
    #                 else:
    #                     continue
    #             else:
    #                 e = Grant.objects.create(**grant, cooperative=instance)
    #                 keep_grants.append(e.id)

    #         for grant in instance.grants.all():
    #             if grant.id not in keep_grants:
    #                 grants.delete()

    #     return instance
    
    class Meta:
        model = Business        
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
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    borrowerType = serializers.CharField(read_only=True)

    tin = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phoneNo = serializers.CharField(read_only=True)
    business = BusinessSerializer()
    documents = DocumentSerializer(many=True)
    borrowerAttachments = BorrowerAttachmentSerializer(many=True)
    totalAvailments = serializers.CharField(read_only=True)
    totalAvailmentPerProgram = serializers.CharField(read_only=True)
    totalOutstandingBalance = serializers.CharField(read_only=True)
    loans = LoanSerializer(many=True,read_only=True)
    creditLines = CreditLineSerializer(many=True,read_only=True)
    payments = PaymentSerializer(many=True,read_only=True)
    totalPayments =  serializers.CharField(read_only=True)
     
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

class CRUDBorrowerSerializer(ModelSerializer):
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        borrower = Borrower.objects.create(**validated_data)

        return borrower
            
    class Meta:
        model = Borrower        
        fields = '__all__'
