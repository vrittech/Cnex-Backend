# Generated by Django 4.1 on 2024-03-19 05:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_productdetailaftervariation_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='description',
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_rating'),
        ),
    ]