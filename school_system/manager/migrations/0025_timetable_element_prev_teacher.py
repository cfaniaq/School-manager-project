# Generated by Django 4.1.1 on 2022-10-19 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0024_alter_subjects_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable_element',
            name='prev_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev_teacher', to='manager.teachers'),
        ),
    ]
