# Generated by Django 4.1.1 on 2022-10-20 08:46

from django.db import migrations, models
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0026_remove_students_timetable_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='lucky_color',
            field=models.CharField(default=manager.models.random_color, max_length=15),
        ),
    ]
