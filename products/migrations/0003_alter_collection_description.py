# Generated by Django 4.1 on 2024-03-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_discount_product_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]