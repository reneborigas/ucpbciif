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
    addressTypeName = serializers.CharField(read_only=True)
    countryName = serializers.CharField(read_only=True)
    ownerLesseeName = serializers.CharField(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('individual','business', )

class IdentificationSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)
    identificationTypeName = serializers.CharField(read_only=True)

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
    contactTypeName = serializers.CharField(read_only=True)
    
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

    nationalityName = serializers.CharField(read_only=True)
    legalFormName = serializers.CharField(read_only=True)
    psicName = serializers.CharField(read_only=True)
    firmSizeName = serializers.CharField(read_only=True)

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

    def update(self, instance, validated_data):
        businessAddress = validated_data.get('businessAddress')
        businessIdentification = validated_data.get('businessIdentification')
        businessContact = validated_data.get('businessContact')
        businessContactPerson = validated_data.get('businessContactPerson')
        businessBackground = validated_data.get('businessBackground')
        businessDirectors = validated_data.get('businessDirectors')
        businessStandingCommittees = validated_data.get('businessStandingCommittees')
        businessGrants = validated_data.get('businessGrants')

        instance.tradeName = validated_data.get("tradeName",instance.tradeName)
        instance.officialRegisteredTradeName = validated_data.get("officialRegisteredTradeName",instance.officialRegisteredTradeName)
        instance.nationality = validated_data.get("nationality",instance.nationality)
        instance.resident = validated_data.get("resident",instance.resident)
        instance.legalForm = validated_data.get("legalForm",instance.legalForm)
        instance.termOfExistence = validated_data.get("termOfExistence",instance.termOfExistence)
        instance.psic = validated_data.get("psic",instance.psic)
        instance.registrationDate = validated_data.get("registrationDate",instance.registrationDate)
        instance.numberOfEmployees = validated_data.get("numberOfEmployees",instance.numberOfEmployees)
        instance.firmSize = validated_data.get("firmSize",instance.firmSize)
        instance.grossIncome = validated_data.get("grossIncome",instance.grossIncome)
        instance.netTaxableIncome = validated_data.get("netTaxableIncome",instance.netTaxableIncome)
        instance.monthlyExpenses = validated_data.get("monthlyExpenses",instance.monthlyExpenses)
        instance.currency = validated_data.get("currency",instance.currency)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.save()


        keep_businessAddress = []        
        if businessAddress:
            for address in businessAddress:
                if 'id' in address.keys():
                    if Address.objects.filter(id=address['id']).exists():   
                        e = Address.objects.get(id=address['id'])
                        e.addressType = address.get('addressType',e.addressType)
                        e.streetNo = address.get('streetNo',e.streetNo)
                        e.postalCode = address.get('postalCode',e.postalCode)
                        e.subdivision = address.get('subdivision',e.subdivision)
                        e.barangay = address.get('barangay',e.barangay)
                        e.city = address.get('city',e.city)
                        e.province = address.get('province',e.province)
                        e.country = address.get('country',e.country)
                        e.ownerLessee = address.get('ownerLessee',e.ownerLessee)
                        e.occupiedSince = address.get('occupiedSince',e.occupiedSince)
                        e.dateUpdated = address.get('dateUpdated',e.dateUpdated)
                        e.save()
                        keep_businessAddress.append(e.id)
                    else:
                        continue
                else:
                    e = Address.objects.create(**address, business=instance)
                    keep_businessAddress.append(e.id)

            for address in instance.businessAddress.all():
                if address.id not in keep_businessAddress:
                    businessAddress.delete()

        keep_businessIdentification = []        
        if businessIdentification:
            for identification in businessIdentification:
                if 'id' in identification.keys():
                    if Identification.objects.filter(id=identification['id']).exists():   
                        e = Identification.objects.get(id=identification['id'])
                        e.identificationType = identification.get('identificationType',e.identificationType)
                        e.identificationNumber = identification.get('identificationNumber',e.identificationNumber)
                        e.dateUpdated = identification.get('dateUpdated',e.dateUpdated)
                        e.save()
                        keep_businessIdentification.append(e.id)
                    else:
                        continue
                else:
                    e = Identification.objects.create(**identification, business=instance)
                    keep_businessIdentification.append(e.id)

            for identification in instance.businessIdentification.all():
                if identification.id not in keep_businessIdentification:
                    businessIdentification.delete()

        keep_businessContact = []        
        if businessContact:
            for contact in businessContact:
                if 'id' in contact.keys():
                    if Contact.objects.filter(id=contact['id']).exists():   
                        e = Contact.objects.get(id=contact['id'])
                        e.contactType = contact.get('contactType',e.contactType)
                        e.contactNumber = contact.get('contactNumber',e.contactNumber)
                        e.dateUpdated = contact.get('dateUpdated',e.dateUpdated)
                        e.save()
                        keep_businessContact.append(e.id)
                    else:
                        continue
                else:
                    e = Contact.objects.create(**contact, business=instance)
                    keep_businessContact.append(e.id)

            for contact in instance.businessContact.all():
                if contact.id not in keep_businessContact:
                    businessContact.delete()

        keep_businessContactPerson = []        
        if businessContactPerson:
            for contactPerson in businessContactPerson:
                if 'id' in contactPerson.keys():
                    if ContactPerson.objects.filter(id=contactPerson['id']).exists():   
                        e = ContactPerson.objects.get(id=contactPerson['id'])
                        e.firstname = contactPerson.get('firstname',e.firstname)
                        e.middlename = contactPerson.get('middlename',e.middlename)
                        e.lastname = contactPerson.get('lastname',e.lastname)
                        e.address = contactPerson.get('address',e.address)
                        e.telNo = contactPerson.get('telNo',e.telNo)
                        e.emailAddress = contactPerson.get('emailAddress',e.emailAddress)
                        e.phoneNo = contactPerson.get('phoneNo',e.phoneNo)
                        e.dateUpdated = contactPerson.get('dateUpdated',e.dateUpdated)
                        e.save()
                        keep_businessContactPerson.append(e.id)
                    else:
                        continue
                else:
                    e = ContactPerson.objects.create(**contactPerson, business=instance)
                    keep_businessContactPerson.append(e.id)

            for contactPerson in instance.businessContactPerson.all():
                if contactPerson.id not in keep_businessContactPerson:
                    businessContactPerson.delete()

        keep_businessBackground = []        
        if businessBackground:
            for background in businessBackground:
                if 'id' in background.keys():
                    if Background.objects.filter(id=background['id']).exists():   
                        e = Background.objects.get(id=background['id'])
                        e.icRiskRating = background.get('icRiskRating',e.icRiskRating)
                        e.cdaRegistrationDate = background.get('cdaRegistrationDate',e.cdaRegistrationDate)
                        e.initialMembershipSize = background.get('initialMembershipSize',e.initialMembershipSize)
                        e.membershipSize = background.get('membershipSize',e.membershipSize)
                        e.paidUpCapitalInitial = background.get('paidUpCapitalInitial',e.paidUpCapitalInitial)
                        e.noOfCooperators = background.get('noOfCooperators',e.noOfCooperators)
                        e.coconutFarmers = background.get('coconutFarmers',e.coconutFarmers)
                        e.authorized = background.get('authorized',e.authorized)
                        e.fullyPaidSharesNo = background.get('fullyPaidSharesNo',e.fullyPaidSharesNo)
                        e.bookValue = background.get('bookValue',e.bookValue)
                        e.parValue = background.get('parValue',e.parValue)
                        e.paidUp = background.get('paidUp',e.paidUp)
                        e.fullyPaidPercent = background.get('fullyPaidPercent',e.fullyPaidPercent)
                        e.initialPaidUpShare = background.get('initialPaidUpShare',e.initialPaidUpShare)
                        e.dateUpdated = background.get('dateUpdated',e.dateUpdated)
                        e.save()
                        keep_businessBackground.append(e.id)
                    else:
                        continue
                else:
                    e = Background.objects.create(**background, business=instance)
                    keep_businessBackground.append(e.id)

            for background in instance.businessBackground.all():
                if background.id not in keep_businessBackground:
                    businessBackground.delete()

        keep_businessDirectors = []        
        if businessDirectors:
            for director in businessDirectors:
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
                        keep_businessDirectors.append(e.id)
                    else:
                        continue
                else:
                    e = Director.objects.create(**director, business=instance)
                    keep_businessDirectors.append(e.id)

            for director in instance.businessDirectors.all():
                if director.id not in keep_businessDirectors:
                    businessDirectors.delete()

        keep_businessStandingCommittees = []        
        if businessStandingCommittees:
            for standingCommittee in businessStandingCommittees:
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
                        keep_businessStandingCommittees.append(e.id)
                    else:
                        continue
                else:
                    e = StandingCommittee.objects.create(**standingCommittee, business=instance)
                    keep_businessStandingCommittees.append(e.id)

            for standingCommittee in instance.businessStandingCommittees.all():
                if standingCommittee.id not in keep_businessStandingCommittees:
                    businessStandingCommittees.delete()

        keep_businessGrants = []        
        if businessGrants:
            for grant in businessGrants:
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
                        keep_businessGrants.append(e.id)
                    else:
                        continue
                else:
                    e = Grant.objects.create(**grant, business=instance)
                    keep_businessGrants.append(e.id)

            for grant in instance.businessGrants.all():
                if grant.id not in keep_businessGrants:
                    businessGrants.delete()

        return instance
    
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
    branchCode = serializers.CharField(read_only=True)

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
        instance.recordType = validated_data.get("recordType",instance.recordType)
        instance.providerCode = validated_data.get("providerCode",instance.providerCode)
        instance.branch = validated_data.get("branch",instance.branch)
        instance.subjectReferenceDate = validated_data.get("subjectReferenceDate",instance.subjectReferenceDate)
        instance.providerSubjectNumber = validated_data.get("providerSubjectNumber",instance.providerSubjectNumber)
        instance.status = validated_data.get("status",instance.status)
        instance.clientSince = validated_data.get("clientSince",instance.clientSince)
        instance.description = validated_data.get("description",instance.description)
        instance.remarks = validated_data.get("remarks",instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
        instance.save()

        return instance
    
    class Meta:
        model = Borrower        
        fields = '__all__'

class CreateBorrowerSerializer(ModelSerializer):
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        borrower = Borrower.objects.create(**validated_data)

        return borrower
            
    class Meta:
        model = Borrower        
        fields = '__all__'

class UpdateBorrowerSerializer(ModelSerializer):
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    business = BusinessSerializer()

    def update(self, instance, validated_data):
        instance.recordType = validated_data.get("recordType",instance.recordType)
        instance.providerCode = validated_data.get("providerCode",instance.providerCode)
        instance.branch = validated_data.get("branch",instance.branch)
        instance.subjectReferenceDate = validated_data.get("subjectReferenceDate",instance.subjectReferenceDate)
        instance.providerSubjectNumber = validated_data.get("providerSubjectNumber",instance.providerSubjectNumber)
        instance.status = validated_data.get("status",instance.status)
        instance.clientSince = validated_data.get("clientSince",instance.clientSince)
        instance.description = validated_data.get("description",instance.description)
        instance.remarks = validated_data.get("remarks",instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated",instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted",instance.isDeleted)
        instance.save()

        return instance
            
    class Meta:
        model = Borrower        
        fields = '__all__'

class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class BorrowerReportSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    branch = serializers.ReadOnlyField(source='branch.branchCode')
    
    window = serializers.ReadOnlyField(source='loans.loanProgram.name')
    loanTerm = serializers.ReadOnlyField(source='loans.term.name')

    totalAvailments = serializers.CharField(read_only=True)
    totalOutstandingBalance = serializers.CharField(read_only=True)
    totalPayments =  serializers.CharField(read_only=True)

    class Meta:
        model = Borrower        
        fields = ['borrowerName','branch','totalAvailments','totalOutstandingBalance','totalPayments','clientSince','window','loanTerm']
