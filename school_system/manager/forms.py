from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from manager.models import (Classes,  Classrooms, Students,
                            Teachers, Timetable_element, Grades,
                             Students_timetable, Assignment, Subjects, Absence)                      
from django.forms import ModelForm
from django import forms
from datetime import datetime
from bootstrap_modal_forms.forms import BSModalModelForm

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", )
		help_texts = {
            'username': None,
            'email': None,
        }
	def __init__(self, *args, **kwargs):
			super(UserCreationForm, self).__init__(*args, **kwargs)        
			self.fields['password1'].help_text = 'The password must be at least 8 characters long'
			self.fields['password2'].help_text = ''

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class TeachersForm(ModelForm):
    class Meta:
        model = Teachers
        fields = ['first_name', 'last_name', 'subjects_taught', 'class_supervised']
        widgets = {
        'subjects_taught': forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(TeachersForm, self).__init__(*args, **kwargs)
        self.fields['class_supervised'].required = False

class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = ['first_name', 'last_name', 'class_attended']
        
    def __init__(self, *args, **kwargs):
        super(StudentsForm, self).__init__(*args, **kwargs)
        self.fields['class_attended'].required = False

class DateInput(forms.DateInput):
    input_type = 'date'
        
class Timetable_elementForm(ModelForm):
    class Meta:
        model = Timetable_element
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'value': datetime.now().strftime("%Y-%m-%d")}),
        }
        labels = {
        "hour": "Period",
        "teacher": "Substitute teacher",
        "prev_teacher": "Previous teacher",
        }
    def __init__(self, *args, **kwargs):
        super(Timetable_elementForm, self).__init__(*args, **kwargs)
        self.fields['prev_teacher'].required = False
        
class Students_timetableForm(ModelForm):
    class Meta:
        model = Students_timetable
        fields = '__all__'
        widgets = {
            
        }
        labels = {
        "classes": "Class name"
        }

class Classes_Form(ModelForm):
    class Meta:
        model = Classes
        fields = '__all__'
        labels = {
        "name": "Class name"
        }

class Classroom_Form(ModelForm):
    class Meta:
        model = Classrooms
        fields = '__all__'
        
class Choose_classForm(ModelForm):
    class Meta:
        model = Students_timetable
        fields = ['classes']
        labels = {
        "classes": "Class number: "
        }
        
class Choose_teacherForm(ModelForm):
    class Meta:
        model = Students_timetable
        fields = ['teacher']
        
class Students_timetableModelForm(BSModalModelForm):
    class Meta:
        model = Students_timetable
        fields = '__all__'

class Choose_class_ModalForm(BSModalModelForm):
    class Meta:
        model = Students_timetable
        fields = ['classes']

class AssignmentModelForm(BSModalModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'value': datetime.now().strftime("%Y-%m-%d")}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
    def __init__(self, *args, **kwargs):
        super(AssignmentModelForm, self).__init__(*args, **kwargs)
        teacher = Teachers.objects.get(user_id = self.request.user.id)
        self.fields['subject'].queryset = teacher.subjects_taught
        
class GradesModelForm(BSModalModelForm):
    class Meta:
        model = Grades
        fields = '__all__'
        
        widgets = {
            'date': DateInput(attrs={'value': datetime.now().strftime("%Y-%m-%d")}),
        }
    def __init__(self, *args, **kwargs):
        super(GradesModelForm, self).__init__(*args, **kwargs)
        teacher = Teachers.objects.get(user_id = self.request.user.id)
        self.fields['subject'].queryset = teacher.subjects_taught
        self.fields['student'].queryset = Students.objects.filter(class_attended = self.request.session['cur_class'])
        self.fields['teacher'].queryset = Teachers.objects.filter(user_id = self.request.user.id)
        self.fields['assignment'].required = False
        self.fields['assignment'].queryset = Assignment.objects.filter(who_created = Teachers.objects.get(user_id = self.request.user.id))
        
class AbsenceModelForm(BSModalModelForm):
    class Meta:
        model = Absence
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'value': datetime.now().strftime("%Y-%m-%d")}),
        }
    def __init__(self, *args, **kwargs):
        super(AbsenceModelForm, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False
        
class TeachersModelForm(BSModalModelForm):
    class Meta:
        model = Teachers
        fields = ['first_name', 'last_name', 'subjects_taught', 'class_supervised']
        widgets = {
        'subjects_taught': forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(TeachersModelForm, self).__init__(*args, **kwargs)
        self.fields['class_supervised'].required = False
        
class StudentsModelForm(BSModalModelForm):
    class Meta:
        model = Students
        fields = ['first_name', 'last_name', 'class_attended']
    def __init__(self, *args, **kwargs):
        super(StudentsModelForm, self).__init__(*args, **kwargs)
        self.fields['class_attended'].required = False
        
class SubstitutionModelForm(BSModalModelForm):
    class Meta:
        model = Timetable_element
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'value': datetime.now().strftime("%Y-%m-%d")}),
        }