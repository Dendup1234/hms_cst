# Generated by Django 5.0.4 on 2024-05-26 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0010_booking_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='user_profile',
        ),
    ]
