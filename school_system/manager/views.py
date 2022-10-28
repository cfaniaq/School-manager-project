from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.views.generic.list import ListView
from datetime import datetime

from manager.models import (Classes,  Students,
                            Teachers, Timetable_element,
                            Students_timetable, 
                             Assignment, Grades, Subjects, Absence,)

from .forms import (Classes_Form, Classroom_Form, StudentsForm, TeachersForm, 
                    Students_timetableModelForm, Choose_classForm, NewUserForm,
                    Choose_teacherForm, AssignmentModelForm, GradesModelForm, AbsenceModelForm, TeachersModelForm, StudentsModelForm, SubstitutionModelForm)

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalDeleteView, BSModalUpdateView
from django.urls import reverse_lazy


@login_required
def which_class(request):
    current_user = request.user.id
    if request.user.groups.filter(name='Students').exists():
        student_which_class = Students.objects.get(user_id = current_user).class_attended_id
        return student_which_class
    else:
        return '0' # just a random number, since it will redirect you if you are not a student anyways

@login_required
def which_teacher(request):
    current_user = request.user.id
    if request.user.groups.filter(name='Teachers').exists():
        c_teacher = Teachers.objects.get(user_id = current_user).id
        return c_teacher
    else:
        return '0'
    
def today_week():
    now = datetime.now()
    t_week = now.strftime("%W")
    return t_week

def today_year():
    now = datetime.now()
    t_year = now.strftime("%Y")
    return t_year

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required    
def index(request):
    template_name = 'manager/index.html'
    context = {'week_nr' : today_week(),
               'student_which_class' : which_class(request),
               'year_nr' : today_year(),}
    return render(request, template_name, context)
    
@login_required
def dashboard(request, week_number, year_number):
    next_week = int(week_number) + 1
    prev_week = int(week_number) - 1
    p_year = year_number
    n_year = year_number
    if week_number == 0:
        p_year = int(year_number) -1
        prev_week = int(week_number) + 53
    if week_number == 53:
        n_year = int(year_number) +1
        next_week = int(week_number) - 53
    
    firstdayofweek = datetime.strptime(f'{year_number}-W{int(week_number )}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + timedelta(days=6.9)
    absences = Absence.objects.filter(date__week=week_number, date__year=year_number).order_by('date')
    students_number = Students.objects.all().count()
    teachers_number = Teachers.objects.all().count()
    pending_notices = Absence.objects.filter(status = 'In progress').count()
    context = {
               'students_number' : students_number,
               'teachers_number' : teachers_number,
               'pending_notices' : pending_notices,
               'absences' : absences,
               'first_day_of_week': firstdayofweek,
               'last_day_of_week': lastdayofweek,
               'next_week': next_week,
               'prev_week': prev_week,
               'week_nr' : today_week(),
               'year_nr' : today_year(),
               'p_year' : p_year,
               'n_year' : n_year,
               'student_which_class' : which_class(request),
               }
    return render(request, 'manager/dashboard.html', context)


def timetable(request, student_which_class, week_number, year_number):
    current_user = request.user.id
    usr_group = str(request.user.groups.all())
    next_week = int(week_number) + 1
    prev_week = int(week_number) - 1
    p_year = year_number
    n_year = year_number
    if week_number == 0:
        p_year = int(year_number) -1
        prev_week = int(week_number) + 53
    if week_number == 53:
        n_year = int(year_number) +1
        next_week = int(week_number) - 53
        
    if 'Students' in usr_group or 'Teachers'in usr_group:
        if 'Students'in usr_group:
            curr_student_name = Students.objects.get(user_id = current_user)
            time_tbl = Timetable_element.objects.filter(classes=which_class(request), date__week=week_number, date__year=year_number)
            student_timetable = Students_timetable.objects.filter(classes=which_class(request))
        if 'Teachers'in usr_group:
            curr_student_name = Teachers.objects.get(user_id = current_user) #even though it's for teachers it's still called students, just co I dont have to make changes to the template
            time_tbl = Timetable_element.objects.filter(teacher=which_teacher(request), date__week=week_number, date__year=year_number) #edit prev_teacher
            student_timetable = Students_timetable.objects.filter(teacher=which_teacher(request))
        iterations = [1,2,3,4,5,6,7,8,9,10,11,12]
        monday_list = []
        tuesday_list = []
        wednesday_list = []
        thursday_list = []
        friday_list = []
        
        for i in iterations:
            monday_list.append(i)
            for e in student_timetable:
                if e.hour == i and e.day_of_week == 1:
                    monday_list.append(e)
                    monday_list.remove(i)
            for t in time_tbl:
                if t.date.strftime("%A") == 'Monday' and t.hour == i:
                    del monday_list[i-1]
                    monday_list.append(t)

            tuesday_list.append(i)
            for e in student_timetable:
                if e.hour == i and e.day_of_week == 2:
                    tuesday_list.append(e)
                    tuesday_list.remove(i)
            for t in time_tbl:
                if t.date.strftime("%A") == 'Tuesday' and t.hour == i:
                    del tuesday_list[i-1]
                    tuesday_list.append(t)
                    
            wednesday_list.append(i)
            for e in student_timetable:
                if e.hour == i and e.day_of_week == 3:
                    wednesday_list.append(e)
                    wednesday_list.remove(i)
            for t in time_tbl:
                if t.date.strftime("%A") == 'Wednesday' and t.hour == i:
                    del wednesday_list[i-1]
                    wednesday_list.append(t)
                    
            thursday_list.append(i)
            for e in student_timetable:
                if e.hour == i and e.day_of_week == 4:
                    thursday_list.append(e)
                    thursday_list.remove(i)
            for t in time_tbl:
                if t.date.strftime("%A") == 'Thursday' and t.hour == i:
                    del thursday_list[i-1]
                    thursday_list.append(t)
                    
            friday_list.append(i)
            for e in student_timetable:
                if e.hour == i and e.day_of_week == 5:
                    friday_list.append(e)
                    friday_list.remove(i)
            for t in time_tbl:
                if t.date.strftime("%A") == 'Friday' and t.hour == i:
                    del friday_list[i-1]
                    friday_list.append(t)


        context = {'time_tbl': time_tbl,
                   'iterations' : iterations,
                    'week_nr' : today_week(),
                    'year_nr' : today_year(),
                    'student_which_class' : which_class(request),
                    'curr_student_name': curr_student_name,
                    'monday_list' : monday_list,
                    'tuesday_list' : tuesday_list,
                    'wednesday_list' : wednesday_list,
                    'thursday_list' : thursday_list,
                    'friday_list' : friday_list,
                    'next_week': next_week,
                    'prev_week': prev_week,
                    'p_year' : p_year,
                    'n_year' : n_year,
                }
        return render(request, 'manager/timetable.html', context)
    else:
        messages.error(request, "You are not a student nor a teacher")
        return redirect("/")

def register_teacher(request):
    if request.method == "POST":
        r_form = NewUserForm(request.POST)
        t_form = TeachersForm(request.POST)
        if r_form.is_valid() and t_form.is_valid():
            user = r_form.save()
            t_form = t_form.save()
            t_form.user = user
            t_form.user_id = user.id
            t_form.save()
            group = Group.objects.get(name='Teachers')
            user.groups.add(group)
            messages.success(request, "Teacher added!" )
            return redirect("/teachers_list")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        r_form = NewUserForm()
        t_form = TeachersForm()
    return render (request, template_name="manager/register_teacher.html", context={"register_form":r_form, 
                                                                                    "teachers_form":t_form, 
                                                                                    'week_nr' : today_week(),
                                                                                    'year_nr' : today_year(),
                                                                                    'student_which_class' : which_class(request),})

class TeachersListView(ListView):
    model = Teachers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teachers.objects.all()
        subjects = Teachers.subjects_taught
        context = {'week_nr' : today_week(),
                  'year_nr' : today_year(),
                  'object_list' : teachers,
                  'subjects' : subjects,
                    'student_which_class' : which_class(self.request)}
        return context

def register_student(request):
    def random_color():
        import random
        list = ['red','green','blue','white','black','purple','orange','yellow','pink','grey']
        return random.choice(list)
    if request.method == "POST":
        r_form = NewUserForm(request.POST)
        s_form = StudentsForm(request.POST)
        if r_form.is_valid() and s_form.is_valid():
            user = r_form.save()
            s_form = s_form.save()
            s_form.user = user
            s_form.user_id = user.id
            s_form.lucky_color = random_color()
            s_form.save()
            
            group = Group.objects.get(name='Students')
            user.groups.add(group)
            messages.success(request, "Student added!" )
            return redirect("/students_list")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        r_form = NewUserForm()
        s_form = StudentsForm()
    return render (request, template_name="manager/register_student.html", context={"register_form":r_form, 
                                                                                    "students_form":s_form, 
                                                                                    'week_nr' : today_week(),
                                                                                    'year_nr' : today_year(),
                                                                                    'student_which_class' : which_class(request),})

class StudentsListView(ListView):
    model = Students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Students.objects.all()
        context = {'week_nr' : today_week(),
                  'year_nr' : today_year(),
                  'object_list' : students,
                  'student_which_class' : which_class(self.request)}
        return context

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="manager/login.html", context={"login_form":form,
                                                                             'week_nr' : today_week(),
                                                                             'year_nr' : today_year(),
                                                                             'student_which_class' : which_class(request),})


@login_required
def logout_view(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/login")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/change_password')
        else:
            messages.error(request, 'Password couldn\'t be changed')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'manager/change_password.html', {
        'change_password_form': form,
        'week_nr' : today_week(),
        'year_nr' : today_year(),
        'student_which_class' : which_class(request),
    })

def create_classes(request):
    if request.method == 'POST':
        form = Classes_Form(request.POST)
        if form.is_valid():
            messages.success(request, "Class added!")
            form.save()
            form = Classes_Form()
            return redirect("/create_classes")
        else:
            messages.error(request, "Class couldn't be added.")
            return redirect("/create_classes")
    else:
        form = Classes_Form() 
    return render(request=request, template_name="manager/create_classes.html", context={"create_classes_form":form, 
                                                                                         'week_nr' : today_week(),
                                                                                         'year_nr' : today_year(),
                                                                                         'student_which_class' : which_class(request),})


def create_classroom(request):
    if request.method == 'POST':
        form = Classroom_Form(request.POST)
        if form.is_valid():
            messages.success(request, "Classroom added!")
            form.save()
            form = Classroom_Form()
            return redirect("/create_classroom")
        else:
            messages.error(request, "Classroom couldn't be added.")
            return redirect("/create_classroom")
    else:
        form = Classroom_Form() 
    return render(request=request, template_name="manager/create_classroom.html", context={"create_classroom_form":form, 
                                                                                           'week_nr' : today_week(),
                                                                                           'year_nr' : today_year(),
                                                                                           'student_which_class' : which_class(request),})

def choose_class(request):
    if request.method == "POST":
        ch_class_form = Choose_classForm(request.POST)
        ch_teach_form = Choose_teacherForm(request.POST)
        if ch_class_form.is_valid():
           c_class = ch_class_form.save(commit=False)
           c_class.save()
           return ('timetable')
        elif ch_teach_form.is_valid():
           c_teach = ch_teach_form.save(commit=False)
           c_teach.save()
           return ('timetable')
    else:
       ch_class_form = Choose_classForm()
       ch_teach_form = Choose_teacherForm()

    return render(request, 'manager/choose_class.html', {'form': ch_class_form,
                                                         't_form' : ch_teach_form,
                                                        'week_nr' : today_week(),
                                                        'year_nr' : today_year(),
                                                        'student_which_class' : which_class(request),})

def class_timetable(request):
    if request.POST.get('classes') != None:
        request.session['cur_class'] = request.POST.get('classes')
        request.session['which'] = 'student'
    
    if request.POST.get('teacher') != None:
        request.session['cur_teacher'] = request.POST.get('teacher')
        request.session['cur_class'] = 2 #Here it means it's class 1A
        request.session['which'] = 'teacher'
    
    if request.session['which'] == 'student' :
        student_timetable = Students_timetable.objects.filter(classes=request.session['cur_class'])
        curr_class_name = Classes.objects.get(id=request.session['cur_class'])
    if request.session['which'] == 'teacher' :   
        student_timetable = Students_timetable.objects.filter(teacher=request.session['cur_teacher'])
        curr_class_name = Teachers.objects.get(id=request.session['cur_teacher']) #teacher name
     

    iterations = [1,2,3,4,5,6,7,8,9,10,11,12]
    monday_list = []
    tuesday_list = []
    wednesday_list = []
    thursday_list = []
    friday_list = []
    
    for i in iterations:
        monday_list.append(i)
        request.session[f'{i}'] = i
        for e in student_timetable:
            if e.hour == i and e.day_of_week == 1:
                monday_list.append(e)
                monday_list.remove(i)

        tuesday_list.append(i)
        for e in student_timetable:
            if e.hour == i and e.day_of_week == 2:
                tuesday_list.append(e)
                tuesday_list.remove(i)
                
        wednesday_list.append(i)
        for e in student_timetable:
            if e.hour == i and e.day_of_week == 3:
                wednesday_list.append(e)
                wednesday_list.remove(i)
                
        thursday_list.append(i)
        for e in student_timetable:
            if e.hour == i and e.day_of_week == 4:
                thursday_list.append(e)
                thursday_list.remove(i)
                
        friday_list.append(i)
        for e in student_timetable:
            if e.hour == i and e.day_of_week == 5:
                friday_list.append(e)
                friday_list.remove(i)

    context = {
                'iterations' : iterations,
                'monday_list' : monday_list,
                'tuesday_list' : tuesday_list,
                'wednesday_list' : wednesday_list,
                'thursday_list' : thursday_list,
                'friday_list' : friday_list,
                'week_nr' : today_week(),
                'year_nr' : today_year(),
                'student_which_class' : which_class(request),
                'classes' : curr_class_name,
            }
    return render(request, 'manager/class_timetable.html', context)

    

class Students_timetableModalView(BSModalCreateView):
    template_name = 'manager/create_timetable.html'
    form_class = Students_timetableModelForm
    success_message = 'Success: Added!'
    success_url = reverse_lazy('manager:class_timetable')
    
    def get_initial(self):
        if is_ajax(request=self.request):
            if self.request.POST.get('which_hour') != None:
                self.request.session['hour'] = self.request.POST.get('which_hour')
                self.request.session['day'] = self.request.POST.get('day_of_week')
            curr_teacher = Teachers.objects.get(id=23)
        if self.request.session['which'] == 'teacher':
            curr_teacher = Teachers.objects.get(id=self.request.session['cur_teacher'])
        else:
            curr_teacher = Teachers.objects.get(id=23)
        curr_class_name = Classes.objects.get(id=self.request.session['cur_class'])
        return {'hour': self.request.session['hour'],
                'day_of_week': self.request.session['day'],
                'classes': curr_class_name,
                'teacher' : curr_teacher,
        }

def t_notices(request):
    cur_teacher = Teachers.objects.get(user_id=request.user.id)
    absences = Absence.objects.filter(teacher = cur_teacher)
    subs = Timetable_element.objects.filter(teacher = cur_teacher)
    
    return render(request, 'manager/teacher_notices.html', {
                                                    'absences' : absences,
                                                    'subs' : subs,
                                                    'week_nr' : today_week(),
                                                    'year_nr' : today_year(),
                                                    'student_which_class' : which_class(request),})




class S_AssignmentsListView(ListView):
    model = Assignment
    template_name = 'manager/student_assignments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignments = Assignment.objects.filter(classes = which_class(self.request)).order_by('date')
        student_class = Classes.objects.get(id = which_class(self.request))
        curr_class = student_class.name
        context = {'week_nr' : today_week(),
                  'year_nr' : today_year(),
                  'object_list' : assignments,
                  'student_which_class' : which_class(self.request),
                  'curr_class' : curr_class}
        return context

class T_AssignmentsListView(ListView):
    model = Assignment
    template_name = 'manager/teacher_assignments.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignments = Assignment.objects.filter(who_created = which_teacher(self.request))
        context = {'week_nr' : today_week(),
                  'year_nr' : today_year(),
                  'object_list' : assignments,
                  'student_which_class' : which_class(self.request)}
        return context
       
class AssignmentModalView(BSModalCreateView):
    template_name = 'manager/create_assignment.html'
    form_class = AssignmentModelForm
    success_message = 'Success: Added!'
    success_url = reverse_lazy('manager:teacher_assignments')
    
    def get_initial(self):
        who_created = which_teacher(self.request)
        return {'who_created': who_created,      
        }
   
def choose_grade_class(request):
    if request.method == "POST":
        ch_class_form = Choose_classForm(request.POST)
        if ch_class_form.is_valid():
           c_class = ch_class_form.save(commit=False)
           c_class.save()
           return ('timetable')
    else:
       ch_class_form = Choose_classForm()
    return render(request, 'manager/choose_grade_class.html', {'form': ch_class_form,
                                                        'week_nr' : today_week(),
                                                        'year_nr' : today_year(),
                                                        'student_which_class' : which_class(request),})
@login_required
def t_grades(request):
    if request.POST.get('classes') != None:
        request.session['cur_class'] = request.POST.get('classes')
    students_list = Students.objects.filter(class_attended = request.session['cur_class']).order_by('last_name')
    curr_class_name = Classes.objects.get(id=request.session['cur_class'])
    cur_teacher = Teachers.objects.get(user_id=request.user.id)
    t_subjects = cur_teacher.subjects_taught.all()
    grades = Grades.objects.filter(teacher = cur_teacher.id)
    return render(request, 'manager/t_grades.html', {
                                                    'class_name' : curr_class_name,
                                                    't_subjects' : t_subjects,
                                                    'grades' : grades,
                                                    'students_list' : students_list,
                                                    'week_nr' : today_week(),
                                                    'year_nr' : today_year(),
                                                    'student_which_class' : which_class(request),})
@login_required
def s_grades(request):
    cur_student = Students.objects.get(user_id=request.user.id)
    subjects = Subjects.objects.all()
    grades = Grades.objects.filter(student = cur_student.id)
    return render(request, 'manager/s_grades.html', {
        'student' : cur_student,
        'subjects' : subjects,
        'grades' : grades,
        'week_nr' : today_week(),
        'year_nr' : today_year(),
        'student_which_class' : which_class(request)
    })
    

class GradeModalView(BSModalCreateView):
    template_name = 'manager/add_grade.html'
    form_class = GradesModelForm
    success_message = 'Success: Added!'
    success_url = reverse_lazy('manager:t_grades')
    def get_initial(self):
        if is_ajax(request=self.request):
            if self.request.POST.get('which_student') != None:
                self.request.session['which_student'] = self.request.POST.get('which_student')
        curr_teacher = Teachers.objects.get(user_id=self.request.user.id)
        curr_class_name = Classes.objects.get(id=self.request.session['cur_class'])
        return {
                'student' : self.request.session['which_student'],
                'classes': curr_class_name,
                'teacher' : curr_teacher,
        }
class Grade_updateView(BSModalUpdateView):
    model = Grades
    template_name = 'manager/edit_grade.html'
    form_class = GradesModelForm
    success_message = 'Success: Edited!'
    success_url = reverse_lazy('manager:t_grades')

class Grade_DeleteView(BSModalDeleteView):
    model = Grades
    template_name = 'manager/delete_grade.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:t_grades')

class AbsenceModalView(BSModalCreateView):
    template_name = 'manager/add_absence.html'
    form_class = AbsenceModelForm
    success_message = 'Success: Added!'
    success_url = reverse_lazy('manager:t_notices')
    def get_initial(self):
        curr_teacher = Teachers.objects.get(user_id=self.request.user.id)
        return {
                'teacher' : curr_teacher,
                'status' : 'In progress',
        }
        
class Assignment_updateView(BSModalUpdateView):
    model = Assignment
    template_name = 'manager/edit_assignment.html'
    form_class = AssignmentModelForm
    success_message = 'Success: Edited!'
    success_url = reverse_lazy('manager:teacher_assignments')

class Assignment_DeleteView(BSModalDeleteView):
    model = Assignment
    template_name = 'manager/delete_assignment.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:teacher_assignments')

class Absence_modalView(BSModalReadView):
    model = Absence
    template_name = 'manager/view_absence.html'

class Absence_updateView(BSModalUpdateView):
    model = Absence
    template_name = 'manager/edit_absence.html'
    form_class = AbsenceModelForm
    success_url = reverse_lazy('manager:dashboard', kwargs={'week_number' : today_week(), 'year_number' : today_year()})
    
class Absence_DeleteView(BSModalDeleteView):
    model = Absence
    template_name = 'manager/delete_absence.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:dashboard', kwargs={'week_number' : today_week(), 'year_number' : today_year()})
    
class Teacher_modalView(BSModalReadView):
    model = Teachers
    template_name = 'manager/view_teacher.html'

class Teacher_updateView(BSModalUpdateView):
    model = Teachers
    template_name = 'manager/edit_teacher.html'
    form_class = TeachersModelForm
    success_message = 'Success: Edited!'
    success_url = reverse_lazy('manager:teachers_list')
    
class Teacher_DeleteView(BSModalDeleteView):
    model = Teachers
    template_name = 'manager/delete_teacher.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:teachers_list')
    
class Student_modalView(BSModalReadView):
    model = Students
    template_name = 'manager/view_student.html'

class Student_updateView(BSModalUpdateView):
    model = Students
    template_name = 'manager/edit_student.html'
    form_class = StudentsModelForm
    success_message = 'Success: Edited!'
    success_url = reverse_lazy('manager:students_list')
    
class Student_DeleteView(BSModalDeleteView):
    model = Students
    template_name = 'manager/delete_student.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:students_list')

class Timetable_elementDeleteView(BSModalDeleteView):
    model = Students_timetable
    template_name = 'manager/delete_tt_element.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:class_timetable')

class SubstitutionsListView(ListView):
    model = Timetable_element
    template_name = 'manager/substitutions.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substitutions = Timetable_element.objects.all().order_by('date')
        context = {'week_nr' : today_week(),
                  'year_nr' : today_year(),
                  'object_list' : substitutions,
                  'student_which_class' : which_class(self.request)}
        return context

class Create_SubstitutionModalView(BSModalCreateView):
    template_name = 'manager/add_substitution.html'
    form_class = SubstitutionModelForm
    success_message = 'Success: Added!'
    success_url = reverse_lazy('manager:substitutions')

class Notice_modalView(BSModalReadView):
    model = Timetable_element
    template_name = 'manager/notice.html'
    
class Substitution_updateView(BSModalUpdateView):
    model = Timetable_element
    template_name = 'manager/edit_sub.html'
    form_class = SubstitutionModelForm
    success_message = 'Success: Edited!'
    success_url = reverse_lazy('manager:substitutions')
    
class Substitution_DeleteView(BSModalDeleteView):
    model = Timetable_element
    template_name = 'manager/delete_sub.html'
    success_message = 'Success: Element was deleted.'
    success_url = reverse_lazy('manager:substitutions') 
    
class Grade_modalView(BSModalReadView):
    model = Grades
    template_name = 'manager/grade.html'
    
class Assignment_modalView(BSModalReadView):
    model = Assignment
    template_name = 'manager/view_assignment.html'
    
class Regular_tt_element_modalView(BSModalReadView):
    model = Students_timetable
    template_name = 'manager/reg_tt_ele.html'


#  filters
 
@register.filter
def get_range(value):
    return range(value)

@register.filter
def plus_one(value):
    return (value+1)

@register.filter
def is_admin(user):
    return user.groups.filter(name='Admins').exists()

@register.filter
def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()

@register.filter
def is_student(user):
    return user.groups.filter(name='Students').exists()

@register.filter
def is_demo(user):
    return user.groups.filter(name='Demo').exists()
