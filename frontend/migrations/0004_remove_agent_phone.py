# Generated by Django 5.0.6 on 2024-09-15 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_alter_agent_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='phone',
        ),
    ]
