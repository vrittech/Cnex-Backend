# Generated by Django 4.1 on 2024-03-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_stock',
            field=models.BooleanField(default=True),
        ),
    ]