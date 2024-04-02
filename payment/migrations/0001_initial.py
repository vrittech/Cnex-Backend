# Generated by Django 4.1 on 2024-04-02 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('appointment', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.FloatField()),
                ('payment_mode', models.CharField(choices=[('khalti', 'Khalti'), ('esewa', 'Esewa'), ('cod', 'Cash On Ddelivery')], max_length=100)),
                ('refrence_id', models.CharField(default='cod', max_length=4000)),
                ('remarks', models.CharField(blank=True, max_length=3000, null=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Paid'), ('half', 'Half Payment'), ('cod', 'Cash On Delivery'), ('refunded', 'Refunded')], max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment', to='appointment.checkoutappointment')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.FloatField()),
                ('payment_mode', models.CharField(choices=[('khalti', 'Khalti'), ('esewa', 'Esewa'), ('cod', 'Cash On Ddelivery')], max_length=100)),
                ('refrence_id', models.CharField(default='cod', max_length=4000)),
                ('remarks', models.CharField(blank=True, max_length=3000, null=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Paid'), ('half', 'Half Payment'), ('cod', 'Cash On Delivery'), ('refunded', 'Refunded')], max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment', to='order.order')),
            ],
        ),
    ]
