# Generated by Django 2.1.7 on 2020-06-05 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0005_auto_20200605_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='committee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committeeSteps', to='committees.Committee'),
        ),
    ]
