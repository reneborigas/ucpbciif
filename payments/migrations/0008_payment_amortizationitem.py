# Generated by Django 2.1.7 on 2020-07-15 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0022_auto_20200714_0033'),
        ('payments', '0007_auto_20200714_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amortizationItem',
            field=models.ForeignKey(default=555, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='loans.AmortizationItem'),
            preserve_default=False,
        ),
    ]
