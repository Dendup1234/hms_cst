# Generated by Django 5.0.4 on 2024-05-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0011_alter_floor_hostel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
