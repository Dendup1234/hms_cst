# Generated by Django 5.0.4 on 2024-05-28 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0019_alter_room_max_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('Vacant', 'Vacant'), ('Full', 'Full'), ('Maintainece', 'Maintainece')], default='Vacant', max_length=200),
        ),
    ]
