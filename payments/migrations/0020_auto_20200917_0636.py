# Generated by Django 2.1.7 on 2020-09-16 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0019_auto_20200917_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='amortizationItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='loans.AmortizationItem'),
        ),
    ]
