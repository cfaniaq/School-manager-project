from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import RegexValidator


# Create your models here.
class Subjects(models.Model):
    subject_name = models.CharField(max_length=30, unique=True, null=False)
    
    class Meta:
        ordering = ['subject_name']
    
    def __str__(self):
         return self.subject_name
    
class Classes(models.Model):
    caps_and_numbers = RegexValidator(r'^[0-9A-Z]*$', 'Only caps and numbers are allowed.')
    name = models.CharField(max_length=6, unique=True, null=True, validators=[caps_and_numbers], help_text='Only numbers and capital letters')
    number_of_students = models.IntegerField(null=False)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
         return self.name
    
class Teachers(models.Model):
    first_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40, null=False)
    subjects_taught = models.ManyToManyField(Subjects)
    class_supervised = models.OneToOneField(Classes, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    user_id = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['last_name']
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Absence(models.Model):
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    status_list = [('In progress', 'In progress'), ('Reviewed', 'Reviewed'), ('Denied', 'Denied')]
    status = models.CharField(choices=status_list, max_length = 30, null=True)
    reason = models.CharField(max_length=300, null=True)
    comments = models.CharField(max_length=300, null=True)
    
    class Meta:
        ordering = ['date']

def random_color(): #it is not needed here, but stays because it is referenced in previous migrations and returns error 
    import random
    list = ['red','green','blue','white','black','purple','orange','yellow','pink','grey']
    return random.choice(list)
    
class Students(models.Model):
    first_name = models.CharField(max_length=40, null=False)
    last_name = models.CharField(max_length=40, null=False)
    class_attended = models.ForeignKey(Classes, on_delete=models.CASCADE, unique=False, null=True, blank=True)
    user_id = models.IntegerField(null=True)
    lucky_color = models.CharField(max_length=15)
    
    class Meta:
        ordering = ['last_name']
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Assignment(models.Model):
    name = models.CharField(max_length=40, null=False)
    type_list = [(1, 'test'), (2, 'quiz')]
    asgn_type = models.IntegerField(choices=type_list)
    who_created = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500, null=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    
    def __str__(self):
        return f'{self.name}'

class Grades(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    type_list = [(1, 'test'),(2, 'activity'), (3, 'quiz'), (4, 'oral answer'), (5,'answer at the blackboard')]
    grade_type = models.IntegerField(choices=type_list, null=True)
    grade_list = [(6, '6'),(5,'5'),(4,'4'),(3,'3'),(2,'2'), (1,'1')]
    grade = models.IntegerField(choices=grade_list)
    date = models.DateField()
    def __str__(self):
        return f'{self.grade}'
    
class Classrooms(models.Model):
    classroom_number = models.CharField(max_length=20, unique=True, null=False)

    class Meta:
        ordering = ['classroom_number']

    def __str__(self):
         return self.classroom_number
    
class Timetable_element(models.Model): #it's actually notices, will change later
    date = models.DateField()
    h_numbers = [
        (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'), 
        (7,'7'), (8,'8'), (9,'9'), (10,'10'), (11,'11'), (12,'12'), 
        ]
    hour = models.IntegerField(choices=h_numbers)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    prev_teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='prev_teacher', null=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    is_sub = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    class Meta:
        constraints = [
        UniqueConstraint(fields=['date', 'hour', 'classroom'], name='classroom_availability'),
        UniqueConstraint(fields=['date', 'hour', 'classes'], name='classes_availability'),
        UniqueConstraint(fields=['date', 'hour', 'teacher'], name='teacher_availability'),
        ]

class Students_timetable(models.Model): #actual timetable that stays the same every week 
    days = [
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')
    ]
    day_of_week = models.IntegerField(choices=days)
    h_numbers = [
        (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'), 
        (7,'7'), (8,'8'), (9,'9'), (10,'10'), (11,'11'), (12,'12'), 
        ]
    hour = models.IntegerField(choices = h_numbers)
    semesters = [
        (1, 'Summer'), (2, 'Winter')
    ]
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    class Meta:
        constraints = [
        UniqueConstraint(fields=['day_of_week', 'hour', 'classroom'], name='s_classroom_availability'),
        UniqueConstraint(fields=['day_of_week', 'hour', 'classes'], name='s_classes_availability'),
        UniqueConstraint(fields=['day_of_week', 'hour', 'teacher'], name='s_teacher_availability'),
        ]
