# Generated by Django 2.1.7 on 2020-07-01 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0008_loanprogram'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='loanProgram',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='programLoans', to='loans.LoanProgram'),
        ),
    ]