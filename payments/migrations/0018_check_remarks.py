# Generated by Django 2.1.7 on 2020-09-16 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0017_auto_20200917_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]