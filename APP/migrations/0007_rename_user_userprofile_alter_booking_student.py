# Generated by Django 5.0.4 on 2024-05-25 19:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0006_rename_user_booking_student'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Userprofile',
        ),
        migrations.AlterField(
            model_name='booking',
            name='student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to=settings.AUTH_USER_MODEL),
        ),
    ]
