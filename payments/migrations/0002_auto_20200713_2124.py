# Generated by Django 2.1.7 on 2020-07-13 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='bankAccount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='checkNo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]