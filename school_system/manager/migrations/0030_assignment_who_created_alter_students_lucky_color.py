# Generated by Django 4.1.1 on 2022-10-20 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0029_assignment_classes_alter_students_lucky_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='who_created',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.teachers'),
        ),
        migrations.AlterField(
            model_name='students',
            name='lucky_color',
            field=models.CharField(default='grey', max_length=15),
        ),
    ]
