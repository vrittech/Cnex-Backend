# Generated by Django 4.1 on 2024-03-19 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compaign', '0002_remove_faqs_imge_remove_privacypolicy_imge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privacypolicy',
            name='title',
        ),
    ]
