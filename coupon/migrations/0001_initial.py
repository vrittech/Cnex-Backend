# Generated by Django 4.1 on 2024-04-02 10:45

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('discount_type', models.CharField(choices=[('flat', 'flat'), ('percentage', 'percentage')], max_length=30)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('from_date', models.DateField(default=django.utils.timezone.now)),
                ('to_date', models.DateField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='coupon/image')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_expired', models.BooleanField(default=False)),
                ('limit', models.PositiveIntegerField()),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
            ],
        ),
    ]
