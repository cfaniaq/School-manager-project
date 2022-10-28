# Generated by Django 4.1.1 on 2022-09-06 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_classes_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable_element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('hour', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')])),
                ('is_sub', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.classes')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.classrooms')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.subjects')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.teachers')),
            ],
        ),
    ]
