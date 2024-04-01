# Generated by Django 4.1 on 2024-04-01 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variations', '0001_initial'),
        ('order', '0004_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='variations',
            field=models.ManyToManyField(blank=True, related_name='order_items', to='variations.variationoption'),
        ),
    ]
