# Generated by Django 2.1.7 on 2020-09-28 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0018_auto_20200928_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.AddField(
            model_name='address',
            name='country1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
