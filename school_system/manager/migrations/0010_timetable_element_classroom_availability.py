# Generated by Django 4.1.1 on 2022-09-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_alter_timetable_element_managers'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='timetable_element',
            constraint=models.UniqueConstraint(fields=('date', 'hour', 'classroom'), name='classroom_availability', violation_error_message='Hejcia'),
        ),
    ]
