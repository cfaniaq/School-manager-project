# Generated by Django 4.1.1 on 2022-10-20 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0031_assignment_subject_alter_assignment_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grades',
            name='grade_type',
            field=models.IntegerField(choices=[(1, 'test'), (2, 'activity'), (3, 'quiz'), (4, 'oral answer'), (5, 'answer at the blackboard')], null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='asgn_type',
            field=models.IntegerField(choices=[(1, 'test'), (2, 'quiz')]),
        ),
        migrations.AlterField(
            model_name='grades',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.assignment'),
        ),
        migrations.AlterField(
            model_name='students',
            name='lucky_color',
            field=models.CharField(default='pink', max_length=15),
        ),
    ]