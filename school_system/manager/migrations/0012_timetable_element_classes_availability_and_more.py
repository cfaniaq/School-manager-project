# Generated by Django 4.1.1 on 2022-09-30 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_remove_timetable_element_classroom_availability_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='timetable_element',
            constraint=models.UniqueConstraint(fields=('date', 'hour', 'classes'), name='classes_availability'),
        ),
        migrations.AddConstraint(
            model_name='timetable_element',
            constraint=models.UniqueConstraint(fields=('date', 'hour', 'teacher'), name='teacher_availability'),
        ),
    ]
