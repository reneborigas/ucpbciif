# Generated by Django 2.1.7 on 2020-09-16 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0044_auto_20200915_2311'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0016_auto_20200816_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateReceived', models.DateTimeField(blank=True, null=True)),
                ('bankBranch', models.CharField(max_length=255)),
                ('checkNo', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('pnNo', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('dateWarehoused', models.DateTimeField(blank=True, null=True)),
                ('warehousingBatchNo', models.DateTimeField(blank=True, null=True)),
                ('amortizationItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amortizationItems', to='loans.AmortizationItem')),
            ],
        ),
        migrations.CreateModel(
            name='CheckStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('isDefault', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkStatusesCreatedBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='check',
            name='checkStatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkStatuses', to='payments.CheckStatus'),
        ),
        migrations.AddField(
            model_name='check',
            name='loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='loans.Loan'),
        ),
    ]
