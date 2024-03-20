# Generated by Django 4.1 on 2024-03-20 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_shippingaddress_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to=settings.AUTH_USER_MODEL),
        ),
    ]
