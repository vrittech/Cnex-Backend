# Generated by Django 4.1 on 2024-04-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='', max_length=15, null=True),
        ),
    ]
