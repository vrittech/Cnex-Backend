# Generated by Django 4.1 on 2024-03-31 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compaign', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpAndSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TermAndCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
    ]