# Generated by Django 2.1.7 on 2020-12-01 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0007_borrowerdocumenttype_religiontype"),
        ("committees", "0008_auto_20200730_0614"),
        ("borrowers", "0027_auto_20201027_2048"),
    ]

    operations = [
        migrations.CreateModel(
            name="BorrowerDocuments",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dateReceived", models.DateTimeField(blank=True, null=True)),
                ("referenceNumber", models.CharField(blank=True, max_length=255, null=True)),
                ("nameOfDocument", models.CharField(blank=True, max_length=255, null=True)),
                ("documentNumber", models.CharField(blank=True, max_length=255, null=True)),
                ("propertyDescription", models.CharField(blank=True, max_length=255, null=True)),
                ("propertyLocation", models.CharField(blank=True, max_length=255, null=True)),
                ("landArea", models.CharField(blank=True, max_length=255, null=True)),
                ("zonalValue", models.CharField(blank=True, max_length=255, null=True)),
                ("appraisalDate", models.DateField(blank=True, null=True)),
                (
                    "appraisalValue",
                    models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
                ),
                ("otherRemarks", models.TextField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CIC",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("providerCode", models.CharField(blank=True, max_length=255, null=True)),
                ("branchCode", models.CharField(blank=True, max_length=255, null=True)),
                ("subjectReferenceDate", models.DateField(blank=True, null=True)),
                ("providerSubjectNumber", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="grant",
            name="business",
        ),
        migrations.RemoveField(
            model_name="grant",
            name="createdBy",
        ),
        migrations.RenameField(
            model_name="borrower",
            old_name="clientSince",
            new_name="accreditationDate",
        ),
        migrations.RenameField(
            model_name="borrower",
            old_name="branch",
            new_name="area",
        ),
        migrations.RemoveField(
            model_name="borrower",
            name="providerCode",
        ),
        migrations.RemoveField(
            model_name="borrower",
            name="providerSubjectNumber",
        ),
        migrations.RemoveField(
            model_name="borrower",
            name="subjectReferenceDate",
        ),
        migrations.RemoveField(
            model_name="contactperson",
            name="address",
        ),
        migrations.RemoveField(
            model_name="standingcommittee",
            name="oSLoanWithCoop",
        ),
        migrations.AddField(
            model_name="borrower",
            name="committee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="borrowerCommittee",
                to="committees.Committee",
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="reRegistrationDate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="barangay",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contactPersonCountry",
                to="settings.Country",
            ),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="postalCode",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="province",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="streetNo",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contactperson",
            name="subdivision",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="individual",
            name="alienCertificateRegistrationNumber",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="individual",
            name="dateOfMarriage",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="individual",
            name="religion",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="individualReligion",
                to="settings.ReligionType",
            ),
        ),
        migrations.AddField(
            model_name="standingcommittee",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="Grant",
        ),
        migrations.AddField(
            model_name="borrowerdocuments",
            name="borrower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="borrowerDocuments", to="borrowers.Borrower"
            ),
        ),
        migrations.AddField(
            model_name="borrowerdocuments",
            name="documentType",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="borrowerDocumentsDocumentType",
                to="settings.BorrowerDocumentType",
            ),
        ),
    ]
