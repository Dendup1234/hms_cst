# Generated by Django 5.0.4 on 2024-05-25 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0008_alter_hostel_id_alter_menu_id_alter_room_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='student',
            new_name='user',
        ),
    ]
