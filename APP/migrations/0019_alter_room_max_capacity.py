# Generated by Django 5.0.4 on 2024-05-28 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0018_alter_floor_number_alter_hostel_name_alter_room_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='max_capacity',
            field=models.IntegerField(default=3),
        ),
    ]