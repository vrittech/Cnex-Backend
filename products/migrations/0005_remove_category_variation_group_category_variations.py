# Generated by Django 4.1 on 2024-03-17 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('variations', '0001_initial'),
        ('products', '0004_alter_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='variation_group',
        ),
        migrations.AddField(
            model_name='category',
            name='variations',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='variations.variationoption'),
        ),
    ]
