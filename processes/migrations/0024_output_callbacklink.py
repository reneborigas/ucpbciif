# Generated by Django 2.1.7 on 2020-07-09 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0023_remove_processrequirement_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='callBackLink',
            field=models.TextField(blank=True, null=True),
        ),
    ]