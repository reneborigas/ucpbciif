from django.db import models
from django.utils import timezone
from datetime import date
from django.db.models import Prefetch, F, Case, When, Value as V, Count, Sum, Q
from django.db.models.functions import Coalesce
from payments.models import Payment
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class CIC(models.Model):
    providerCode = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    branchCode = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    subjectReferenceDate = models.DateField(
        null=True,
        blank=True,
    )
    providerSubjectNumber = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )


class Branch(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    address = models.TextField(
        blank=True,
        null=True,
    )
    branchCode = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, related_name="branchCreatedBy", null=True, blank=True
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.name, self.branchCode)


class AnnotatedBusinessManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                _borrowerBusinessNationalityName=F("nationality__description"),
                _borrowerBusinessLegalFormName=F("legalForm__description"),
                _borrowerBusinessPsicName=F("psic__description"),
                _borrowerBusinessFirmSizeName=F("firmSize__description"),
            )
        )


# CIC Compliance
class Business(models.Model):
    tradeName = models.CharField(max_length=255, null=True, blank=True)
    officialRegisteredTradeName = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="businessNationality", null=True, blank=True
    )
    resident = models.BooleanField(
        default=True,
    )
    legalForm = models.ForeignKey(
        "settings.LegalFormType", on_delete=models.SET_NULL, related_name="businessLegalForm", null=True, blank=True
    )
    entityRegistered = models.CharField(max_length=255, null=True, blank=True)
    termOfExistence = models.DateField(null=True, blank=True)
    psic = models.ForeignKey(
        "settings.PSIC", on_delete=models.SET_NULL, related_name="businessPSIC", null=True, blank=True
    )
    registrationDate = models.DateField(null=True, blank=True)
    reRegistrationDate = models.DateField(null=True, blank=True)
    numberOfEmployees = models.IntegerField(null=True, blank=True)
    firmSize = models.ForeignKey(
        "settings.Currency", on_delete=models.SET_NULL, related_name="businessFirmSize", null=True, blank=True
    )
    grossIncome = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    netTaxableIncome = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    monthlyExpenses = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    currency = models.ForeignKey(
        "settings.Currency", on_delete=models.SET_NULL, related_name="businessCurrency", null=True, blank=True
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "%s" % (self.tradeName)


class AnnotatedIndividualManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                _borrowerIndividualTitleName=F("title__description"),
                _borrowerIndividualGenderName=F("gender__description"),
                _borrowerIndividualCountryOfBirthName=F("countryOfBirth__description"),
                _borrowerIndividualNationalityName=F("nationality__description"),
                _borrowerIndividualMaritalStatusName=F("maritalStatus__description"),
                _borrowerIndividualReligionName=F("religion__name"),
            )
        )


# CIC Compliance
class Individual(models.Model):
    title = models.ForeignKey(
        "settings.TitleType", on_delete=models.SET_NULL, related_name="individualTitle", null=True, blank=True
    )
    firstname = models.CharField(max_length=255, null=True, blank=True)
    middlename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    lastname = models.CharField(max_length=255, null=True, blank=True)
    suffix = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    nickname = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    previousLastName = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    gender = models.ForeignKey(
        "settings.GenderType", on_delete=models.SET_NULL, related_name="individualGender", null=True, blank=True
    )
    dateOfBirth = models.DateField(null=True, blank=True)
    placeOfBirth = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    countryOfBirth = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="individualCountryOfBirth", null=True, blank=True
    )
    nationality = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="individualNationality", null=True, blank=True
    )
    resident = models.BooleanField(
        default=True,
    )
    alienCertificateRegistrationNumber = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    maritalStatus = models.ForeignKey(
        "settings.CivilStatusType",
        on_delete=models.SET_NULL,
        related_name="individualCivilStatus",
        null=True,
    )
    religion = models.ForeignKey(
        "settings.ReligionType",
        on_delete=models.SET_NULL,
        related_name="individualReligion",
        null=True,
    )
    dateOfMarriage = models.DateField(null=True, blank=True)
    numberOfDependents = models.IntegerField(null=True, blank=True)
    carsOwned = models.IntegerField(null=True, blank=True)
    numberOfChildren = models.IntegerField(null=True, blank=True)
    educationalAttainment = models.CharField(max_length=255, null=True, blank=True)
    grossSalary = models.CharField(max_length=255, null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    objects = AnnotatedIndividualManager()

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)


# CIC Compliance Individual Foreign Key
class Family(models.Model):
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="individualFamily", null=True, blank=True
    )
    spouseFirstName = models.CharField(max_length=255, null=True, blank=True)
    spouseLastName = models.CharField(max_length=255, null=True, blank=True)
    spouseMiddleName = models.CharField(max_length=255, null=True, blank=True)
    motherMaidenFirstName = models.CharField(max_length=255, null=True, blank=True)
    motherMaidenLastName = models.CharField(max_length=255, null=True, blank=True)
    motherMaidenMiddleName = models.CharField(max_length=255, null=True, blank=True)
    fatherFirstName = models.CharField(max_length=255, null=True, blank=True)
    fatherLastName = models.CharField(max_length=255, null=True, blank=True)
    fatherMiddleName = models.CharField(max_length=255, null=True, blank=True)
    fatherSuffix = models.CharField(max_length=255, null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "%s" % (self.individual)


# CIC Compliance Individual and Business Foreign Key
class Address(models.Model):
    individual = models.ForeignKey(
        Individual,
        on_delete=models.SET_NULL,
        related_name="individualAddress",
        null=True,
        blank=True,
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessAddress",
        null=True,
        blank=True,
    )
    addressType = models.ForeignKey(
        "settings.AddressType", on_delete=models.SET_NULL, related_name="addressAddressType", null=True, blank=True
    )
    streetNo = models.CharField(max_length=255, null=True, blank=True)
    postalCode = models.CharField(max_length=255, null=True, blank=True)
    subdivision = models.CharField(max_length=255, null=True, blank=True)
    barangay = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="addressCountry", null=True, blank=True
    )
    ownerLessee = models.ForeignKey(
        "settings.HouseOwnerLesseeType",
        on_delete=models.SET_NULL,
        related_name="individualAddressOwnerLessee",
        null=True,
        blank=True,
    )
    occupiedSince = models.DateField(null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        if self.business:
            return "%s" % (self.business)
        else:
            return "%s" % (self.individual)


# CIC Compliance Individual and Business Foreign Key
class Identification(models.Model):
    individual = models.ForeignKey(
        Individual,
        on_delete=models.SET_NULL,
        related_name="individualIdentification",
        null=True,
        blank=True,
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessIdentification",
        null=True,
        blank=True,
    )
    identificationType = models.ForeignKey(
        "settings.IdentificationType",
        on_delete=models.SET_NULL,
        related_name="identificationIdentificationType",
        null=True,
    )
    identificationNumber = models.CharField(max_length=255, null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        if self.business:
            return "%s" % (self.business)
        else:
            return "%s" % (self.individual)


# CIC Compliance Individual Foreign Key
class ID(models.Model):
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="individualID", null=True, blank=True
    )
    idType = models.ForeignKey(
        "settings.IDType", on_delete=models.SET_NULL, related_name="individualID", null=True, blank=True
    )
    idNumber = models.CharField(max_length=255, null=True, blank=True)
    idIssueDate = models.DateField(null=True, blank=True)
    idIssueCountry = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="individualIDCountry", null=True, blank=True
    )
    idExpiryDate = models.DateField(null=True, blank=True)
    isIssuedBy = models.CharField(max_length=255, null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "%s" % (self.individual)


# CIC Compliance Individual and Business Foreign Key
class Contact(models.Model):
    individual = models.ForeignKey(
        Individual,
        on_delete=models.SET_NULL,
        related_name="individualContact",
        null=True,
        blank=True,
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessContact",
        null=True,
        blank=True,
    )
    contactType = models.ForeignKey(
        "settings.ContactType", on_delete=models.SET_NULL, related_name="contactContactType", null=True, blank=True
    )
    contactNumber = models.CharField(max_length=255, null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        if self.business:
            return "%s" % (self.business)
        else:
            return "%s" % (self.individual)


# CIC Compliance Individual Foreign Key
class Employment(models.Model):
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="individualEmployment", null=True, blank=True
    )
    tradeName = models.CharField(max_length=255, null=True, blank=True)
    tin = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=255, null=True, blank=True)
    psic = models.ForeignKey(
        "settings.PSIC", on_delete=models.SET_NULL, related_name="individualEmploymentPSIC", null=True, blank=True
    )
    grossIncome = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    incomeIndicator = models.ForeignKey(
        "settings.IncomePeriod",
        on_delete=models.SET_NULL,
        related_name="individualEmploymentIncomeIndicator",
        null=True,
        blank=True,
    )
    currency = models.ForeignKey(
        "settings.Currency",
        on_delete=models.SET_NULL,
        related_name="individualEmploymentCurrency",
        null=True,
        blank=True,
    )
    occupationStatus = models.ForeignKey(
        "settings.OccupationStatusType",
        on_delete=models.SET_NULL,
        related_name="individualEmploymentOccupationStatus",
        null=True,
        blank=True,
    )
    dateHiredFrom = models.DateField(null=True, blank=True)
    dateHiredTo = models.DateField(null=True, blank=True)
    occupation = models.ForeignKey(
        "settings.PSOC", on_delete=models.SET_NULL, related_name="individualEmploymentPSOC", null=True, blank=True
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    natureOfBusiness = models.CharField(max_length=255, null=True, blank=True)
    jobTitle = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.individual)


# CIC Compliance Individual Foreign Key
class SoleTrader(models.Model):
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="individualSoleTrader", null=True, blank=True
    )
    tradeName = models.CharField(max_length=255, null=True, blank=True)
    addressType = models.ForeignKey(
        "settings.AddressType",
        on_delete=models.SET_NULL,
        related_name="individualSoleTraderAddress",
        null=True,
        blank=True,
    )
    streetNo = models.CharField(max_length=255, null=True, blank=True)
    postalCode = models.CharField(max_length=255, null=True, blank=True)
    subdivision = models.CharField(max_length=255, null=True, blank=True)
    barangay = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="individualSoleTraderAddress", null=True, blank=True
    )
    ownerLessee = models.ForeignKey(
        "settings.HouseOwnerLesseeType",
        on_delete=models.SET_NULL,
        related_name="individualSoleTraderOwnerLessee",
        null=True,
        blank=True,
    )
    occupiedSince = models.DateField(null=True, blank=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "%s" % (self.individual)


# Individual Foreign Key
class IndividualBusiness(models.Model):
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE, related_name="individualIndividualBusiness", null=True, blank=True
    )
    nameOfBusiness = models.CharField(max_length=255, null=True, blank=True)
    natureOfBusiness = models.CharField(max_length=255, null=True, blank=True)
    yearsInBusiness = models.CharField(max_length=255, null=True, blank=True)
    grossIncome = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    telNo = models.CharField(max_length=255, null=True, blank=True)
    faxNo = models.CharField(max_length=255, null=True, blank=True)
    streetNo = models.CharField(max_length=255, null=True, blank=True)
    postalCode = models.CharField(max_length=255, null=True, blank=True)
    subdivision = models.CharField(max_length=255, null=True, blank=True)
    barangay = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(
        "settings.Country",
        on_delete=models.SET_NULL,
        related_name="individualBusinessPersonCountry",
        null=True,
        blank=True,
    )

    def __str__(self):
        return "%s" % (self.individual)


# Business Foreign Key
class ContactPerson(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessContactPerson",
        null=True,
        blank=True,
    )
    firstname = models.CharField(max_length=255, null=True, blank=True)
    middlename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    lastname = models.CharField(max_length=255, null=True, blank=True)
    streetNo = models.CharField(max_length=255, null=True, blank=True)
    postalCode = models.CharField(max_length=255, null=True, blank=True)
    subdivision = models.CharField(max_length=255, null=True, blank=True)
    barangay = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(
        "settings.Country", on_delete=models.SET_NULL, related_name="contactPersonCountry", null=True, blank=True
    )
    telNo = models.CharField(max_length=255, null=True, blank=True)
    emailAddress = models.CharField(max_length=255, null=True, blank=True)
    phoneNo = models.CharField(max_length=255, null=True, blank=True)
    createdBy = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, related_name="contactPersonCreatedBy", null=True, blank=True
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.business)


# Business Foreign Key
class Background(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessBackground",
        null=True,
        blank=True,
    )
    icRiskRating = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    # ncorporations
    cdaRegistrationDate = models.DateField(
        null=True,
        blank=True,
    )
    initialMembershipSize = models.IntegerField(null=True, blank=True)
    membershipSize = models.IntegerField(null=True, blank=True)
    paidUpCapitalInitial = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    noOfCooperators = models.IntegerField(null=True, blank=True)
    coconutFarmers = models.IntegerField(null=True, blank=True)
    # capital structure
    authorized = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    fullyPaidSharesNo = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    bookValue = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    parValue = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    paidUp = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    fullyPaidPercent = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    initialPaidUpShare = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "%s" % (self.business)


# Business Foreign Key
class Director(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessDirectors",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    educationalAttainment = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    yearsInCoop = models.IntegerField(null=True, blank=True)
    oSLoanWithCoop = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    address = models.TextField(
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, related_name="directorCreatedBy", null=True, blank=True
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.business)


# Business Foreign Key
class StandingCommittee(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        related_name="businessStandingCommittees",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    educationalAttainment = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    yearsInCoop = models.IntegerField(null=True, blank=True)
    address = models.TextField(
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, related_name="standingCommitteeCreatedBy", null=True, blank=True
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.business)


class Borrower(models.Model):
    borrowerId = models.AutoField(primary_key=True)
    individual = models.OneToOneField(
        Individual,
        on_delete=models.SET_NULL,
        related_name="borrowerIndividual",
        null=True,
        blank=True,
    )
    business = models.OneToOneField(
        Business,
        on_delete=models.SET_NULL,
        related_name="borrowerBusiness",
        null=True,
        blank=True,
    )
    recordType = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    area = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="borrowerBranch",
        null=True,
        blank=True,
        default=6,
    )
    committee = models.ForeignKey(
        "committees.Committee",
        on_delete=models.SET_NULL,
        related_name="borrowerCommittee",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    accreditationDate = models.DateField(
        null=True,
        blank=True,
    )
    reasonForBorrowing = models.TextField(
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser", on_delete=models.SET_NULL, related_name="borrowerCreatedBy", null=True, blank=True
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        if self.individual:
            return "%s" % (self.individual)
        else:
            return "%s" % (self.business)

    def getTotalAvailments(self):
        if not self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ):
            return 0

        loans = self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        )
        totalAvailments = 0
        for loan in loans:
            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal()
            totalAvailments = totalAvailments + loan.totalAmortizationPrincipal

        return totalAvailments

    def getTotalOutstandingBalance(self):
        if not self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ):
            return 0
        totalBalance = 0
        for loan in self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ):

            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal()

            balance = loan.totalAmortizationPrincipal - loan.getTotalPrincipalPayment()
            totalBalance = totalBalance + balance
            print(totalBalance)

        return totalBalance

    def getTotalAvailmentsPerProgram(self, loanProgramId):
        if not self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED"),
            loanProgram_id=loanProgramId,
        ):
            return 0
        return self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED"),
            loanProgram_id=loanProgramId,
        ).aggregate(totalAvailments=Sum(F("amount")))["totalAvailments"]

    def getPayments(self):
        return (
            Payment.objects.filter(loan__borrower=self)
            .annotate(pnNo=F("loan__pnNo"))
            .exclude(isDeleted=True)
            .order_by("-id")
        )

    def getTotalPayments(self):
        return (
            Payment.objects.filter(loan__borrower=self, paymentStatus__name="TENDERED")
            .exclude(isDeleted=True)
            .aggregate(totalPayments=Coalesce(Sum(F("total")), 0))["totalPayments"]
        )


def attachment_directory_path(instance, filename):
    # ext = filename.split('.')[-1]
    # filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return "attachments/borrowers/{0}/{1}".format(instance.borrower.borrowerId, filename)


class BorrowerDocuments(models.Model):
    borrower = models.ForeignKey(
        Borrower,
        on_delete=models.CASCADE,
        related_name="borrowerDocuments",
    )
    dateReceived = models.DateTimeField(blank=True, null=True)
    referenceNumber = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    documentType = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    nameOfDocument = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    documentNumber = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    propertyDescription = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    propertyLocation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    landArea = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    zonalValue = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    appraisalDate = models.DateField(null=True, blank=True)
    appraisalValue = models.DecimalField(default=0, decimal_places=2, max_digits=20, blank=True, null=True)
    otherRemarks = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )


class BorrowerAttachment(models.Model):
    fileName = models.CharField(max_length=255, null=True, blank=True)
    fileAttachment = models.FileField(null=True, blank=True, upload_to=attachment_directory_path)
    borrower = models.ForeignKey(
        Borrower,
        on_delete=models.CASCADE,
        related_name="borrowerAttachments",
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="borrowerAttachmentCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.borrower, self.fileName)
