# Generated by Django 2.1.7 on 2020-07-28 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0032_remove_loan_loanstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='loanStatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='loanStatuses', to='loans.LoanStatus'),
            preserve_default=False,
        ),
    ]