# Generated by Django 4.1 on 2024-04-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order_at',
            field=models.PositiveIntegerField(default=1),
        ),
    ]