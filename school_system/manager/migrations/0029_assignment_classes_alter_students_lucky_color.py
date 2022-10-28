# Generated by Django 4.1.1 on 2022-10-20 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0028_assignment_alter_students_lucky_color_grades'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='classes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.classes'),
        ),
        migrations.AlterField(
            model_name='students',
            name='lucky_color',
            field=models.CharField(default='red', max_length=15),
        ),
    ]