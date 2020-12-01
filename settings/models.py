from django.db import models


class AppName(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    iconAsHTML = models.TextField(
        blank=True,
        null=True,
    )
    navDirectory = models.TextField(
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="appNameCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "App Name (System Essential)"
        verbose_name_plural = "App Names (System Essential)"


class TitleType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="titleTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Title Type (System Essential - CIC)"
        verbose_name_plural = "Title Types (System Essential - CIC)"


class GenderType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="genderTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Gender Type (System Essential - CIC)"
        verbose_name_plural = "Gender Types (System Essential - CIC)"


class Country(models.Model):
    code = models.CharField(
        max_length=255,
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
        related_name="countryCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.code)

    class Meta:
        verbose_name = "Country (System Essential - CIC)"
        verbose_name_plural = "Countries (System Essential - CIC)"


class CivilStatusType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="civilStatusTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Civil Status Type (System Essential - CIC)"
        verbose_name_plural = "Civil Status Types (System Essential - CIC)"


class IdentificationType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="identificationTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.value, self.description)

    class Meta:
        verbose_name = "Identification Type (System Essential - CIC)"
        verbose_name_plural = "Identification Types (System Essential - CIC)"


class IDType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="idCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s - %s" % (self.value, self.description)

    class Meta:
        verbose_name = "ID Type (System Essential - CIC)"
        verbose_name_plural = "ID Types (System Essential - CIC)"


class HouseOwnerLesseeType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="houseOwnerLesseeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "House Owner Lessee Type (System Essential - CIC)"
        verbose_name_plural = "House Owner Lessee Types (System Essential - CIC)"


class AddressType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="addressCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Address Type (System Essential - CIC)"
        verbose_name_plural = "Address Types (System Essential - CIC)"


class ContactType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="contactTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Contact Type (System Essential - CIC)"
        verbose_name_plural = "Contact Types (System Essential - CIC)"


class PSIC(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="psicCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "PSIC Type (System Essential - CIC)"
        verbose_name_plural = "PSIC Types (System Essential - CIC)"


class PSOC(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="psocCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "PSOC Type (System Essential - CIC)"
        verbose_name_plural = "PSOC Types (System Essential - CIC)"


class IncomePeriod(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="incomePeriodCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Income Period Type (System Essential - CIC)"
        verbose_name_plural = "Income Period Types (System Essential - CIC)"


class Currency(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="currencyCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Currency Type (System Essential - CIC)"
        verbose_name_plural = "Currency Types (System Essential - CIC)"


class OccupationStatusType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="occupationStatusTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Occupation Status Type (System Essential - CIC)"
        verbose_name_plural = "Occupation Status Types (System Essential - CIC)"


class LegalFormType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="legalFormTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Legal Form Type (System Essential - CIC)"
        verbose_name_plural = "Legal Form Types (System Essential - CIC)"


class FirmSizeType(models.Model):
    value = models.CharField(
        max_length=255,
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
        related_name="firmSizeTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.value)

    class Meta:
        verbose_name = "Firm Size Type (System Essential - CIC)"
        verbose_name_plural = "Firm Size Types (System Essential - CIC)"


class CooperativeType(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
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
        related_name="cooperativeTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Cooperative Type (System Essential)"
        verbose_name_plural = "Cooperative Types (System Essential)"


class ReligionType(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
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
        related_name="religionTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Religion Type (System Essential)"
        verbose_name_plural = "Religion Types (System Essential)"


class BorrowerDocumentType(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
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
        related_name="borrowerDocumentTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Borrower Document Type (System Essential)"
        verbose_name_plural = "Borrower Document Types (System Essential)"