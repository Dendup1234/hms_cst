# Generated by Django 5.0.4 on 2024-05-28 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0016_counselor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_pic',
        ),
        migrations.AlterField(
            model_name='floor',
            name='number',
            field=models.IntegerField(default=0, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='hostel',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='room',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='reg_number',
            field=models.IntegerField(default=0, null=True, unique=True),
        ),
    ]
