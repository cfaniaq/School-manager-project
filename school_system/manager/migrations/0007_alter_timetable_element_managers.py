# Generated by Django 4.1.1 on 2022-09-09 10:37

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_remove_classrooms_occupied'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='timetable_element',
            managers=[
                ('is_classroom_available', django.db.models.manager.Manager()),
            ],
        ),
    ]
