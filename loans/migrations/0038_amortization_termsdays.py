# Generated by Django 2.1.7 on 2020-08-17 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0037_auto_20200817_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='amortization',
            name='termsDays',
            field=models.PositiveIntegerField(default=0),
        ),
    ]