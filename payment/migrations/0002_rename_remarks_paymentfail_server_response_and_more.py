# Generated by Django 4.1 on 2024-04-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentfail',
            old_name='remarks',
            new_name='server_response',
        ),
        migrations.AlterField(
            model_name='paymentfail',
            name='refrence_id',
            field=models.CharField(max_length=4000),
        ),
    ]