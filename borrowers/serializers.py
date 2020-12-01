from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from documents.serializers import DocumentSerializer
from processes.serializers import SubProcessSerializer
from loans.serializers import LoanSerializer, CreditLineSerializer
from payments.serializers import PaymentSerializer


class FamilySerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Family
        fields = "__all__"
        read_only_fields = ("individual",)


class AddressSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)
    addressTypeName = serializers.CharField(read_only=True)
    countryName = serializers.CharField(read_only=True)
    ownerLesseeName = serializers.CharField(read_only=True)

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = (
            "individual",
            "business",
        )


class IdentificationSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)
    identificationTypeName = serializers.CharField(read_only=True)

    class Meta:
        model = Identification
        fields = "__all__"
        read_only_fields = (
            "individual",
            "business",
        )


class IDSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ID
        fields = "__all__"
        read_only_fields = ("individual",)


class ContactSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)
    contactTypeName = serializers.CharField(read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ("individual", "business")


class EmploymentSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Employment
        fields = "__all__"
        read_only_fields = ("individual",)


class SoleTraderSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SoleTrader
        fields = "__all__"
        read_only_fields = ("individual",)


class IndividualBusinessSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = IndividualBusiness
        fields = "__all__"
        read_only_fields = ("individual",)


class ContactPersonSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ContactPerson
        fields = "__all__"
        read_only_fields = ("business",)


class BackgroundSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Background
        fields = "__all__"
        read_only_fields = ("business",)


class DirectorSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Director
        fields = "__all__"
        read_only_fields = ("business",)


class StandingCommitteeSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = StandingCommittee
        fields = "__all__"
        read_only_fields = ("business",)


class IndividualSerializer(ModelSerializer):
    individualFamily = FamilySerializer(many=True, required=False)
    individualAddress = AddressSerializer(many=True, required=False)
    individualIdentification = IdentificationSerializer(many=True, required=False)
    individualID = IDSerializer(many=True, required=False)
    individualContact = ContactSerializer(many=True, required=False)
    individualEmployment = EmploymentSerializer(many=True, required=False)
    individualIndividualBusiness = IndividualBusinessSerializer(many=True, required=False)
    individualSoleTrader = SoleTraderSerializer(many=True, required=False)

    nationalityName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        individualFamily = validated_data.pop("individualFamily")
        individualAddress = validated_data.pop("individualAddress")
        individualIdentification = validated_data.pop("individualIdentification")
        individualID = validated_data.pop("individualID")
        individualContact = validated_data.pop("individualContact")
        individualEmployment = validated_data.pop("individualEmployment")
        individualIndividualBusiness = validated_data.pop("individualIndividualBusiness")
        individualSoleTrader = validated_data.pop("individualSoleTrader")

        individual = Individual.objects.create(**validated_data)

        for family in individualFamily:
            Family.objects.create(**family, individual=individual)

        for address in individualAddress:
            Address.objects.create(**address, individual=individual)

        for identification in individualIdentification:
            Identification.objects.create(**identification, individual=individual)

        for ind in individualID:
            ID.objects.create(**ind, individual=individual)

        for contact in individualContact:
            Contact.objects.create(**contact, individual=individual)

        for employment in individualEmployment:
            Employment.objects.create(**employment, individual=individual)

        for individualBusiness in individualIndividualBusiness:
            IndividualBusiness.objects.create(**individualBusiness, individual=individual)

        for soleTrader in individualSoleTrader:
            SoleTrader.objects.create(**soleTrader, individual=individual)

        return individual

    def update(self, instance, validated_data):
        individualFamily = validated_data.get("individualFamily")
        individualAddress = validated_data.get("individualAddress")
        individualIdentification = validated_data.get("individualIdentification")
        individualID = validated_data.get("individualID")
        individualContact = validated_data.get("individualContact")
        individualEmployment = validated_data.get("individualEmployment")
        individualIndividualBusiness = validated_data.get("individualIndividualBusiness")
        individualSoleTrader = validated_data.get("individualSoleTrader")

        instance.title = validated_data.get("title", instance.title)
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.middlename = validated_data.get("middlename", instance.middlename)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.suffix = validated_data.get("suffix", instance.suffix)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.previousLastName = validated_data.get("previousLastName", instance.previousLastName)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.dateOfBirth = validated_data.get("dateOfBirth", instance.dateOfBirth)
        instance.placeOfBirth = validated_data.get("placeOfBirth", instance.placeOfBirth)
        instance.countryOfBirth = validated_data.get("countryOfBirth", instance.countryOfBirth)
        instance.nationality = validated_data.get("nationality", instance.nationality)
        instance.resident = validated_data.get("resident", instance.resident)
        instance.alienCertificateRegistrationNumber = validated_data.get(
            "alienCertificateRegistrationNumber", instance.alienCertificateRegistrationNumber
        )
        instance.maritalStatus = validated_data.get("maritalStatus", instance.maritalStatus)
        instance.religion = validated_data.get("religion", instance.religion)
        instance.dateOfMarriage = validated_data.get("dateOfMarriage", instance.dateOfMarriage)
        instance.numberOfDependents = validated_data.get("numberOfDependents", instance.numberOfDependents)
        instance.carsOwned = validated_data.get("carsOwned", instance.carsOwned)
        instance.numberOfChildren = validated_data.get("numberOfChildren", instance.numberOfChildren)
        instance.educationalAttainment = validated_data.get("educationalAttainment", instance.educationalAttainment)
        instance.grossSalary = validated_data.get("grossSalary", instance.grossSalary)
        instance.dateUpdated = validated_data.get("dateUpdated", instance.dateUpdated)

        instance.save()

        keep_individualFamily = []
        if individualFamily:
            for family in individualFamily:
                if "id" in family.keys():
                    if Family.objects.filter(id=family["id"]).exists():
                        e = Family.objects.get(id=family["id"])
                        e.spouseFirstName = family.get("spouseFirstName", e.spouseFirstName)
                        e.spouseLastName = family.get("spouseLastName", e.spouseLastName)
                        e.spouseMiddleName = family.get("spouseMiddleName", e.spouseMiddleName)
                        e.motherMaidenFirstName = family.get("motherMaidenFirstName", e.motherMaidenFirstName)
                        e.motherMaidenLastName = family.get("motherMaidenLastName", e.motherMaidenLastName)
                        e.motherMaidenMiddleName = family.get("motherMaidenMiddleName", e.motherMaidenMiddleName)
                        e.fatherFirstName = family.get("fatherFirstName", e.fatherFirstName)
                        e.fatherLastName = family.get("fatherLastName", e.fatherLastName)
                        e.fatherMiddleName = family.get("fatherMiddleName", e.fatherMiddleName)
                        e.fatherSuffix = family.get("fatherSuffix", e.fatherSuffix)
                        e.dateUpdated = family.get("dateUpdated", e.dateUpdated)
                        e.save()
                        keep_individualFamily.append(e.id)
                    else:
                        continue
                else:
                    e = Family.objects.create(**family, business=instance)
                    keep_individualFamily.append(e.id)

            for family in instance.individualFamily.all():
                if family.id not in keep_individualFamily:
                    individualFamily.delete()

        keep_individualAddress = []
        if individualAddress:
            for address in individualAddress:
                if "id" in address.keys():
                    if Address.objects.filter(id=address["id"]).exists():
                        e = Address.objects.get(id=address["id"])
                        e.addressType = address.get("addressType", e.addressType)
                        e.streetNo = address.get("streetNo", e.streetNo)
                        e.postalCode = address.get("postalCode", e.postalCode)
                        e.subdivision = address.get("subdivision", e.subdivision)
                        e.barangay = address.get("barangay", e.barangay)
                        e.city = address.get("city", e.city)
                        e.province = address.get("province", e.province)
                        e.country = address.get("country", e.country)
                        e.ownerLessee = address.get("ownerLessee", e.ownerLessee)
                        e.occupiedSince = address.get("occupiedSince", e.occupiedSince)
                        e.dateUpdated = address.get("dateUpdated", e.dateUpdated)
                        e.save()
                        keep_individualAddress.append(e.id)
                    else:
                        continue
                else:
                    e = Address.objects.create(**address, business=instance)
                    keep_individualAddress.append(e.id)

            for address in instance.individualAddress.all():
                if address.id not in keep_individualAddress:
                    individualAddress.delete()

        keep_individualIdentification = []
        if individualIdentification:
            for identification in individualIdentification:
                if "id" in identification.keys():
                    if Identification.objects.filter(id=identification["id"]).exists():
                        e = Identification.objects.get(id=identification["id"])
                        e.identificationType = identification.get("identificationType", e.identificationType)
                        e.identificationNumber = identification.get("identificationNumber", e.identificationNumber)
                        e.dateUpdated = identification.get("dateUpdated", e.dateUpdated)
                        e.save()
                        keep_individualIdentification.append(e.id)
                    else:
                        continue
                else:
                    e = Identification.objects.create(**identification, business=instance)
                    keep_individualIdentification.append(e.id)

            for identification in instance.individualIdentification.all():
                if identification.id not in keep_individualIdentification:
                    individualIdentification.delete()

        keep_individualID = []
        if individualID:
            for ind in individualID:
                if "id" in ind.keys():
                    if ID.objects.filter(id=ind["id"]).exists():
                        e = ID.objects.get(id=ind["id"])
                        e.idType = ind.get("idType", e.idType)
                        e.idNumber = ind.get("idNumber", e.idNumber)
                        e.idIssueDate = ind.get("idIssueDate", e.idIssueDate)
                        e.idIssueCountry = ind.get("idIssueCountry", e.idIssueCountry)
                        e.idExpiryDate = ind.get("idExpiryDate", e.idExpiryDate)
                        e.isIssuedBy = ind.get("isIssuedBy", e.isIssuedBy)
                        e.dateUpdated = ind.get("dateUpdated", e.dateUpdated)
                        e.save()
                        keep_individualID.append(e.id)
                    else:
                        continue
                else:
                    e = ID.objects.create(**ind, business=instance)
                    keep_individualID.append(e.id)

            for ind in instance.individualID.all():
                if ind.id not in keep_individualID:
                    individualID.delete()

        keep_individualContact = []
        if individualContact:
            for contact in individualContact:
                if "id" in contact.keys():
                    if Contact.objects.filter(id=contact["id"]).exists():
                        e = Contact.objects.get(id=contact["id"])
                        e.contactType = contact.get("contactType", e.contactType)
                        e.contactNumber = contact.get("contactNumber", e.contactNumber)
                        e.save()
                        keep_individualContact.append(e.id)
                    else:
                        continue
                else:
                    e = Contact.objects.create(**contact, business=instance)
                    keep_individualContact.append(e.id)

            for contact in instance.individualContact.all():
                if contact.id not in keep_individualContact:
                    individualContact.delete()

        keep_individualEmployment = []
        if individualEmployment:
            for employment in individualEmployment:
                if "id" in employment.keys():
                    if Employment.objects.filter(id=employment["id"]).exists():
                        e = Employment.objects.get(id=employment["id"])
                        e.tradeName = employment.get("tradeName", e.tradeName)
                        e.tin = employment.get("tin", e.tin)
                        e.phoneNumber = employment.get("phoneNumber", e.phoneNumber)
                        e.psic = employment.get("psic", e.psic)
                        e.grossIncome = employment.get("grossIncome", e.grossIncome)
                        e.incomeIndicator = employment.get("incomeIndicator", e.incomeIndicator)
                        e.currency = employment.get("currency", e.currency)
                        e.occupationStatus = employment.get("occupationStatus", e.occupationStatus)
                        e.dateHiredFrom = employment.get("dateHiredFrom", e.dateHiredFrom)
                        e.dateHiredTo = employment.get("dateHiredTo", e.dateHiredTo)
                        e.occupation = employment.get("occupation", e.occupation)
                        e.dateUpdated = employment.get("dateUpdated", e.dateUpdated)
                        e.natureOfBusiness = employment.get("natureOfBusiness", e.natureOfBusiness)
                        e.jobTitle = employment.get("jobTitle", e.jobTitle)
                        e.save()
                        keep_individualEmployment.append(e.id)
                    else:
                        continue
                else:
                    e = Employment.objects.create(**employment, business=instance)
                    keep_individualEmployment.append(e.id)

            for employment in instance.individualEmployment.all():
                if employment.id not in keep_individualEmployment:
                    individualEmployment.delete()

        keep_individualIndividualBusiness = []
        if individualIndividualBusiness:
            for business in individualIndividualBusiness:
                if "id" in business.keys():
                    if IndividualBusiness.objects.filter(id=business["id"]).exists():
                        e = IndividualBusiness.objects.get(id=business["id"])
                        e.nameOfBusiness = business.get("nameOfBusiness", e.nameOfBusiness)
                        e.natureOfBusiness = business.get("natureOfBusiness", e.natureOfBusiness)
                        e.yearsInBusiness = business.get("yearsInBusiness", e.yearsInBusiness)
                        e.grossIncome = business.get("grossIncome", e.grossIncome)
                        e.telNo = business.get("telNo", e.telNo)
                        e.faxNo = business.get("faxNo", e.faxNo)
                        e.streetNo = business.get("streetNo", e.streetNo)
                        e.postalCode = business.get("postalCode", e.postalCode)
                        e.subdivision = business.get("subdivision", e.subdivision)
                        e.barangay = business.get("barangay", e.barangay)
                        e.city = business.get("city", e.city)
                        e.province = business.get("province", e.province)
                        e.country = business.get("country", e.country)
                        e.save()
                        keep_individualIndividualBusiness.append(e.id)
                    else:
                        continue
                else:
                    e = IndividualBusiness.objects.create(**business, business=instance)
                    keep_individualIndividualBusiness.append(e.id)

            for business in instance.individualIndividualBusiness.all():
                if business.id not in keep_individualIndividualBusiness:
                    individualIndividualBusiness.delete()

        keep_individualSoleTrader = []
        if individualSoleTrader:
            for soleTrader in individualSoleTrader:
                if "id" in soleTrader.keys():
                    if SoleTrader.objects.filter(id=soleTrader["id"]).exists():
                        e = SoleTrader.objects.get(id=soleTrader["id"])
                        e.tradeName = soleTrader.get("tradeName", e.tradeName)
                        e.addressType = soleTrader.get("addressType", e.addressType)
                        e.streetNo = soleTrader.get("streetNo", e.streetNo)
                        e.postalCode = soleTrader.get("postalCode", e.postalCode)
                        e.subdivision = soleTrader.get("subdivision", e.subdivision)
                        e.barangay = soleTrader.get("barangay", e.barangay)
                        e.city = soleTrader.get("city", e.city)
                        e.province = soleTrader.get("province", e.province)
                        e.country = soleTrader.get("country", e.country)
                        e.ownerLessee = soleTrader.get("ownerLessee", e.ownerLessee)
                        e.occupiedSince = soleTrader.get("occupiedSince", e.occupiedSince)
                        e.dateUpdated = soleTrader.get("dateUpdated", e.dateUpdated)
                        e.save()
                        keep_individualSoleTrader.append(e.id)
                    else:
                        continue
                else:
                    e = ID.objects.create(**soleTrader, business=instance)
                    keep_individualSoleTrader.append(e.id)

            for soleTrader in instance.individualSoleTrader.all():
                if soleTrader.id not in keep_individualSoleTrader:
                    individualSoleTrader.delete()

        return instance

    class Meta:
        model = Individual
        fields = "__all__"


class BusinessSerializer(ModelSerializer):
    businessAddress = AddressSerializer(many=True, required=False)
    businessIdentification = IdentificationSerializer(many=True, required=False)
    businessContact = ContactSerializer(many=True, required=False)
    businessContactPerson = ContactPersonSerializer(many=True, required=False)
    businessBackground = BackgroundSerializer(many=True, required=False)
    businessDirectors = DirectorSerializer(many=True, required=False)
    businessStandingCommittees = StandingCommitteeSerializer(many=True, required=False)

    nationalityName = serializers.CharField(read_only=True)
    legalFormName = serializers.CharField(read_only=True)
    psicName = serializers.CharField(read_only=True)
    firmSizeName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        businessAddress = validated_data.pop("businessAddress")
        businessIdentification = validated_data.pop("businessIdentification")
        businessContact = validated_data.pop("businessContact")
        businessContactPerson = validated_data.pop("businessContactPerson")
        businessBackground = validated_data.pop("businessBackground")
        businessDirectors = validated_data.pop("businessDirectors")
        businessStandingCommittees = validated_data.pop("businessStandingCommittees")

        business = Business.objects.create(**validated_data)

        for address in businessAddress:
            Address.objects.create(**address, business=business)

        for identification in businessIdentification:
            Identification.objects.create(**identification, business=business)

        for contact in businessContact:
            Contact.objects.create(**contact, business=business)

        for contactPerson in businessContactPerson:
            ContactPerson.objects.create(**contactPerson, business=business)

        for background in businessBackground:
            Background.objects.create(**background, business=business)

        for directors in businessDirectors:
            Director.objects.create(**directors, business=business)

        for standingCommittee in businessStandingCommittees:
            StandingCommittee.objects.create(**standingCommittee, business=business)

        return business

    def update(self, instance, validated_data):
        businessAddress = validated_data.get("businessAddress")
        businessIdentification = validated_data.get("businessIdentification")
        businessContact = validated_data.get("businessContact")
        businessContactPerson = validated_data.get("businessContactPerson")
        businessBackground = validated_data.get("businessBackground")
        businessDirectors = validated_data.get("businessDirectors")
        businessStandingCommittees = validated_data.get("businessStandingCommittees")

        instance.tradeName = validated_data.get("tradeName", instance.tradeName)
        instance.officialRegisteredTradeName = validated_data.get(
            "officialRegisteredTradeName", instance.officialRegisteredTradeName
        )
        instance.nationality = validated_data.get("nationality", instance.nationality)
        instance.resident = validated_data.get("resident", instance.resident)
        instance.legalForm = validated_data.get("legalForm", instance.legalForm)
        instance.entityRegistered = validated_data.get("entityRegistered", instance.entityRegistered)
        instance.termOfExistence = validated_data.get("termOfExistence", instance.termOfExistence)
        instance.psic = validated_data.get("psic", instance.psic)
        instance.registrationDate = validated_data.get("registrationDate", instance.registrationDate)
        instance.reRegistrationDate = validated_data.get("reRegistrationDate", instance.reRegistrationDate)
        instance.numberOfEmployees = validated_data.get("numberOfEmployees", instance.numberOfEmployees)
        instance.firmSize = validated_data.get("firmSize", instance.firmSize)
        instance.grossIncome = validated_data.get("grossIncome", instance.grossIncome)
        instance.netTaxableIncome = validated_data.get("netTaxableIncome", instance.netTaxableIncome)
        instance.monthlyExpenses = validated_data.get("monthlyExpenses", instance.monthlyExpenses)
        instance.currency = validated_data.get("currency", instance.currency)
        instance.dateUpdated = validated_data.get("dateUpdated", instance.dateUpdated)
        instance.save()

        keep_businessAddress = []
        if businessAddress:
            for address in businessAddress:
                if "id" in address.keys():
                    if Address.objects.filter(id=address["id"]).exists():
                        e = Address.objects.get(id=address["id"])
                        e.addressType = address.get("addressType", e.addressType)
                        e.streetNo = address.get("streetNo", e.streetNo)
                        e.postalCode = address.get("postalCode", e.postalCode)
                        e.subdivision = address.get("subdivision", e.subdivision)
                        e.barangay = address.get("barangay", e.barangay)
                        e.city = address.get("city", e.city)
                        e.province = address.get("province", e.province)
                        e.country = address.get("country", e.country)
                        e.ownerLessee = address.get("ownerLessee", e.ownerLessee)
                        e.occupiedSince = address.get("occupiedSince", e.occupiedSince)
                        e.dateUpdated = address.get("dateUpdated", e.dateUpdated)
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
                if "id" in identification.keys():
                    if Identification.objects.filter(id=identification["id"]).exists():
                        e = Identification.objects.get(id=identification["id"])
                        e.identificationType = identification.get("identificationType", e.identificationType)
                        e.identificationNumber = identification.get("identificationNumber", e.identificationNumber)
                        e.dateUpdated = identification.get("dateUpdated", e.dateUpdated)
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
                if "id" in contact.keys():
                    if Contact.objects.filter(id=contact["id"]).exists():
                        e = Contact.objects.get(id=contact["id"])
                        e.contactType = contact.get("contactType", e.contactType)
                        e.contactNumber = contact.get("contactNumber", e.contactNumber)
                        e.dateUpdated = contact.get("dateUpdated", e.dateUpdated)
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
                if "id" in contactPerson.keys():
                    if ContactPerson.objects.filter(id=contactPerson["id"]).exists():
                        e = ContactPerson.objects.get(id=contactPerson["id"])
                        e.firstname = contactPerson.get("firstname", e.firstname)
                        e.middlename = contactPerson.get("middlename", e.middlename)
                        e.lastname = contactPerson.get("lastname", e.lastname)
                        e.streetNo = contactPerson.get("streetNo", e.streetNo)
                        e.postalCode = contactPerson.get("postalCode", e.postalCode)
                        e.subdivision = contactPerson.get("subdivision", e.subdivision)
                        e.barangay = contactPerson.get("barangay", e.barangay)
                        e.city = contactPerson.get("city", e.city)
                        e.province = contactPerson.get("province", e.province)
                        e.country = contactPerson.get("country", e.country)
                        e.telNo = contactPerson.get("telNo", e.telNo)
                        e.emailAddress = contactPerson.get("emailAddress", e.emailAddress)
                        e.phoneNo = contactPerson.get("phoneNo", e.phoneNo)
                        e.dateUpdated = contactPerson.get("dateUpdated", e.dateUpdated)
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
                if "id" in background.keys():
                    if Background.objects.filter(id=background["id"]).exists():
                        e = Background.objects.get(id=background["id"])
                        e.icRiskRating = background.get("icRiskRating", e.icRiskRating)
                        e.cdaRegistrationDate = background.get("cdaRegistrationDate", e.cdaRegistrationDate)
                        e.initialMembershipSize = background.get("initialMembershipSize", e.initialMembershipSize)
                        e.membershipSize = background.get("membershipSize", e.membershipSize)
                        e.paidUpCapitalInitial = background.get("paidUpCapitalInitial", e.paidUpCapitalInitial)
                        e.noOfCooperators = background.get("noOfCooperators", e.noOfCooperators)
                        e.coconutFarmers = background.get("coconutFarmers", e.coconutFarmers)
                        e.authorized = background.get("authorized", e.authorized)
                        e.fullyPaidSharesNo = background.get("fullyPaidSharesNo", e.fullyPaidSharesNo)
                        e.bookValue = background.get("bookValue", e.bookValue)
                        e.parValue = background.get("parValue", e.parValue)
                        e.paidUp = background.get("paidUp", e.paidUp)
                        e.fullyPaidPercent = background.get("fullyPaidPercent", e.fullyPaidPercent)
                        e.initialPaidUpShare = background.get("initialPaidUpShare", e.initialPaidUpShare)
                        e.dateUpdated = background.get("dateUpdated", e.dateUpdated)
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
                if "id" in director.keys():
                    if Director.objects.filter(id=director["id"]).exists():
                        e = Director.objects.get(id=director["id"])
                        e.name = director.get("name", e.name)
                        e.position = director.get("position", e.position)
                        e.educationalAttainment = director.get("educationalAttainment", e.educationalAttainment)
                        e.age = director.get("age", e.age)
                        e.yearsInCoop = director.get("yearsInCoop", e.yearsInCoop)
                        e.oSLoanWithCoop = director.get("oSLoanWithCoop", e.oSLoanWithCoop)
                        e.status = director.get("status", e.status)
                        e.dateUpdated = director.get("dateUpdated", e.dateUpdated)
                        e.isDeleted = director.get("isDeleted", e.isDeleted)
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
                if "id" in standingCommittee.keys():
                    if StandingCommittee.objects.filter(id=standingCommittee["id"]).exists():
                        e = StandingCommittee.objects.get(id=standingCommittee["id"])
                        e.name = standingCommittee.get("name", e.name)
                        e.department = standingCommittee.get("department", e.department)
                        e.position = standingCommittee.get("position", e.position)
                        e.educationalAttainment = standingCommittee.get(
                            "educationalAttainment", e.educationalAttainment
                        )
                        e.age = standingCommittee.get("age", e.age)
                        e.yearsInCoop = standingCommittee.get("yearsInCoop", e.yearsInCoop)
                        e.address = standingCommittee.get("address", e.address)
                        e.status = standingCommittee.get("status", e.status)
                        e.dateUpdated = standingCommittee.get("dateUpdated", e.dateUpdated)
                        e.isDeleted = standingCommittee.get("isDeleted", e.isDeleted)
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

        return instance

    class Meta:
        model = Business
        fields = "__all__"


class BorrowerDocumentsSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = BorrowerDocuments
        fields = "__all__"
        read_only_fields = ("borrower",)


class BorrowerAttachmentSerializer(ModelSerializer):
    def create(self, validated_data):
        borrowerAttachment = BorrowerAttachment.objects.create(**validated_data)

        return borrowerAttachment

    def update(self, instance, validated_data):
        instance.save()

        return instance

    class Meta:
        model = BorrowerAttachment
        fields = "__all__"


class BorrowerSerializer(ModelSerializer):
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    borrowerType = serializers.CharField(read_only=True)
    branch = serializers.CharField(read_only=True)

    tin = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phoneNo = serializers.CharField(read_only=True)
    individual = IndividualSerializer()
    business = BusinessSerializer()
    documents = DocumentSerializer(many=True)
    borrowerAttachments = BorrowerAttachmentSerializer(many=True)
    totalAvailments = serializers.CharField(read_only=True)
    totalAvailmentPerProgram = serializers.CharField(read_only=True)
    totalOutstandingBalance = serializers.CharField(read_only=True)
    loans = LoanSerializer(many=True, read_only=True)
    creditLines = CreditLineSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    totalPayments = serializers.CharField(read_only=True)

    def create(self, validated_data):
        borrower = Borrower.objects.create(**validated_data)

        return borrower

    def createLoanApplication(self, validated_data):
        borrower = Borrower.objects.create(**validated_data)

        return borrower

    def update(self, instance, validated_data):
        instance.recordType = validated_data.get("recordType", instance.recordType)
        instance.providerCode = validated_data.get("providerCode", instance.providerCode)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.subjectReferenceDate = validated_data.get("subjectReferenceDate", instance.subjectReferenceDate)
        instance.providerSubjectNumber = validated_data.get("providerSubjectNumber", instance.providerSubjectNumber)
        instance.status = validated_data.get("status", instance.status)
        instance.clientSince = validated_data.get("clientSince", instance.clientSince)
        instance.description = validated_data.get("description", instance.description)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated", instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted", instance.isDeleted)
        instance.save()

        return instance

    class Meta:
        model = Borrower
        fields = "__all__"


class CreateBorrowerSerializer(ModelSerializer):
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    borrowerDocuments = BorrowerDocumentsSerializer(many=True, required=False)

    def create(self, validated_data):
        borrowerDocuments = validated_data.pop("borrowerDocuments")

        borrower = Borrower.objects.create(**validated_data)

        for documents in borrowerDocuments:
            BorrowerDocuments.objects.create(**documents, borrower=borrower)

        return borrower

    class Meta:
        model = Borrower
        fields = "__all__"


class UpdateBorrowerSerializer(ModelSerializer):
    individualName = serializers.CharField(read_only=True)
    businessTradeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    individual = IndividualSerializer()
    business = BusinessSerializer()

    def update(self, instance, validated_data):
        instance.recordType = validated_data.get("recordType", instance.recordType)
        instance.providerCode = validated_data.get("providerCode", instance.providerCode)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.subjectReferenceDate = validated_data.get("subjectReferenceDate", instance.subjectReferenceDate)
        instance.providerSubjectNumber = validated_data.get("providerSubjectNumber", instance.providerSubjectNumber)
        instance.status = validated_data.get("status", instance.status)
        instance.clientSince = validated_data.get("clientSince", instance.clientSince)
        instance.description = validated_data.get("description", instance.description)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.dateUpdated = validated_data.get("dateUpdated", instance.dateUpdated)
        instance.isDeleted = validated_data.get("isDeleted", instance.isDeleted)
        instance.save()

        return instance

    class Meta:
        model = Borrower
        fields = "__all__"


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class BorrowerReportSerializer(ModelSerializer):
    borrowerName = serializers.CharField(read_only=True)
    branch = serializers.ReadOnlyField(source="branch.branchCode")

    window = serializers.ReadOnlyField(source="loans.loanProgram.name")
    loanTerm = serializers.ReadOnlyField(source="loans.term.name")

    totalAvailments = serializers.CharField(read_only=True)
    totalOutstandingBalance = serializers.CharField(read_only=True)
    totalPayments = serializers.CharField(read_only=True)

    class Meta:
        model = Borrower
        fields = [
            "borrowerName",
            "branch",
            "totalAvailments",
            "totalOutstandingBalance",
            "totalPayments",
            "clientSince",
            "window",
            "loanTerm",
        ]
