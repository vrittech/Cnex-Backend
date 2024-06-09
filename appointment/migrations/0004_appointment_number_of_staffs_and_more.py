# Generated by Django 4.1 on 2024-06-06 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_servicesitems_slots'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='number_of_staffs',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='service_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slots_from_time',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slots_to_time',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]