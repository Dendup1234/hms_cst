# Generated by Django 5.0.4 on 2024-05-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0007_rename_user_userprofile_alter_booking_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
