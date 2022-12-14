# Generated by Django 4.1.1 on 2022-09-06 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_alter_teachers_class_supervised'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='name',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='class_supervised',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.classes', unique=True),
        ),
    ]
