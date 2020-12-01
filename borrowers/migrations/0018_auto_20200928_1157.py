# Generated by Django 2.1.7 on 2020-09-28 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0017_auto_20200910_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addressCountry', to='settings.Country'),
        ),
    ]
