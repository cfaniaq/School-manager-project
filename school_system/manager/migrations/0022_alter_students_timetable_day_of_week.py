# Generated by Django 4.1.1 on 2022-10-07 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0021_alter_students_timetable_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students_timetable',
            name='day_of_week',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')]),
        ),
    ]
