# Generated by Django 5.0.4 on 2024-05-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0002_user_room_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=200, null=True),
        ),
    ]
