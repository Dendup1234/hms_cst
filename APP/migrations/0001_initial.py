# Generated by Django 5.0.4 on 2024-05-18 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200)),
                ('image', models.ImageField(upload_to='hostels/')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=200)),
                ('breakfast_description', models.CharField(max_length=200)),
                ('breakfast_image', models.ImageField(upload_to='breakfasts/')),
                ('lunch_description', models.CharField(max_length=200)),
                ('lunch_image', models.ImageField(upload_to='lunches/')),
                ('dinner_description', models.CharField(max_length=200)),
                ('dinner_image', models.ImageField(upload_to='dinners/')),
            ],
        ),
        migrations.CreateModel(
            name='Hostel_description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.TextField()),
                ('hostel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature', to='APP.hostel')),
            ],
        ),
    ]