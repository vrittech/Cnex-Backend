# Generated by Django 4.1 on 2024-08-16 05:18

import accounts.utilities.model_utils
import accounts.utilities.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=accounts.utilities.model_utils.LowercaseEmailField(error_messages={'unique': 'Given Email has already been registered.'}, max_length=254, unique=True, validators=[accounts.utilities.validators.validate_emails], verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, default=None, error_messages={'unique': 'Given Mobile Number has already been registered.'}, max_length=15, null=True, validators=[accounts.utilities.validators.validate_mobile_number], verbose_name='Mobile Number'),
        ),
    ]