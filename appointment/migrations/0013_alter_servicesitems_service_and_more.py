# Generated by Django 4.1 on 2024-03-28 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0012_alter_appointment_checkout_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesitems',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments_items', to='appointment.services'),
        ),
        migrations.AlterField(
            model_name='servicesitems',
            name='slots',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='appointments_items', to='appointment.slots'),
        ),
        migrations.AddConstraint(
            model_name='servicesitems',
            constraint=models.UniqueConstraint(fields=('checkout_appointment', 'slots'), name='checkout_service_slots_unique'),
        ),
    ]