# Generated by Django 2.1.7 on 2020-07-01 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0010_auto_20200701_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanprogram',
            name='creditLineAmount',
            field=models.DecimalField(decimal_places=2, default=4000000, max_digits=12),
            preserve_default=False,
        ),
    ]
