# Generated by Django 2.1.7 on 2020-06-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0018_subprocess_relatedprocesses'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuses',
            name='isFinalStatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statuses',
            name='isNegativeResult',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='step',
            name='position',
            field=models.ManyToManyField(blank=True, to='committees.Position'),
        ),
        migrations.AlterField(
            model_name='subprocess',
            name='relatedProcesses',
            field=models.ManyToManyField(blank=True, to='processes.SubProcess'),
        ),
    ]