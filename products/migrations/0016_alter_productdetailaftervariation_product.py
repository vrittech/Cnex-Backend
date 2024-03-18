# Generated by Django 4.1 on 2024-03-18 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_is_manage_stock_alter_product_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetailaftervariation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='products.product'),
        ),
    ]
