# Generated by Django 5.0.7 on 2024-07-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='document',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Documento de Identidad'),
        ),
    ]
