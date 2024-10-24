# Generated by Django 5.0.7 on 2024-07-18 16:02

import apps.companies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_rename_credencial_credential'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default=apps.companies.models.default_logo, null=True, upload_to='logos_empresas/', verbose_name='Logo'),
        ),
    ]
