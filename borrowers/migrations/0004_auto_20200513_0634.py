# Generated by Django 2.1.7 on 2020-05-13 06:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0003_auto_20200511_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperative',
            name='cdaRegistrationDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]