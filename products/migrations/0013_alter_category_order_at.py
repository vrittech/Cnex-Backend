# Generated by Django 4.1 on 2024-05-05 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_category_order_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='order_at',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]