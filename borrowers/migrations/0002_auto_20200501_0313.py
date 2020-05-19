# Generated by Django 2.1.7 on 2020-05-01 03:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('settings', '0003_auto_20200501_0313'),
        ('borrowers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=255, null=True)),
                ('middlename', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('telNo', models.CharField(blank=True, max_length=255, null=True)),
                ('emailAddress', models.CharField(blank=True, max_length=255, null=True)),
                ('phoneNo', models.CharField(blank=True, max_length=255, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contactPersonCreatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icRiskRating', models.CharField(blank=True, max_length=255, null=True)),
                ('tin', models.CharField(blank=True, max_length=255, null=True)),
                ('cdaRegistrateionDate', models.DateTimeField(default=datetime.date.today)),
                ('initialMembershipSize', models.IntegerField()),
                ('membershipSize', models.IntegerField()),
                ('paidUpCapitalInitial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('noOfCooperators', models.IntegerField()),
                ('coconutFarmers', models.IntegerField()),
                ('authorized', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('fullyPaidSharesNo', models.IntegerField()),
                ('bookValue', models.IntegerField()),
                ('parValue', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('paidUp', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('fullyPaidPercent', models.IntegerField()),
                ('initialPaidUpShare', models.IntegerField()),
                ('address', models.TextField(blank=True, null=True)),
                ('telNo', models.CharField(blank=True, max_length=255, null=True)),
                ('emailAddress', models.CharField(blank=True, max_length=255, null=True)),
                ('phoneNo', models.CharField(blank=True, max_length=255, null=True)),
                ('fax', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('cooperativeType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cooperativeCooperativeType', to='settings.CooperativeType')),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cooperativeCreatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('educationalAttainment', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('yearsInCooop', models.IntegerField()),
                ('oSLoanWithCoop', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('cooperative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directors', to='borrowers.Cooperative')),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directorCreatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor', models.CharField(max_length=255)),
                ('projectType', models.CharField(max_length=255)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('projectStatus', models.CharField(blank=True, max_length=255, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('cooperative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grants', to='borrowers.Cooperative')),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grantCreatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StandingCommittee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('educationalAttainment', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('yearsInCooop', models.IntegerField()),
                ('oSLoanWithCoop', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, max_length=256, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('cooperative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='standingCommittees', to='borrowers.Cooperative')),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='standingCommitteeCreatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='borrower',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='borrower',
            name='description',
        ),
        migrations.RemoveField(
            model_name='borrower',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='borrower',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='borrower',
            name='middlename',
        ),
        migrations.AddField(
            model_name='borrower',
            name='clientSince',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='borrower',
            name='dateUpdated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='borrower',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrowerCreatedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='PersonalInfo',
        ),
        migrations.AddField(
            model_name='borrower',
            name='contactPerson',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrowerContactPerson', to='borrowers.ContactPerson'),
        ),
        migrations.AddField(
            model_name='borrower',
            name='cooperative',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrowerCooperative', to='borrowers.Cooperative'),
        ),
    ]