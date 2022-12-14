# Generated by Django 4.1.1 on 2022-10-20 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0027_students_lucky_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('asgn_type', models.IntegerField(choices=[(1, 'test'), (2, 'activity'), (3, 'quiz'), (4, 'oral answer'), (5, 'answer at the blackboard')])),
                ('description', models.CharField(max_length=40, null=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='students',
            name='lucky_color',
            field=models.CharField(default='grey', max_length=15),
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(choices=[(6, 'A'), (5, 'B'), (4, 'C'), (3, 'D'), (2, 'E'), (1, 'F')])),
                ('date', models.DateField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.students')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.subjects')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.teachers')),
            ],
        ),
    ]
