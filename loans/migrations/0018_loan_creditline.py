# Generated by Django 2.1.7 on 2020-07-10 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0017_auto_20200709_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='creditLine',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='loans.CreditLine'),
            preserve_default=False,
        ),
    ]