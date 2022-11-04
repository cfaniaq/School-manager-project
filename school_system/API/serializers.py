from django.contrib.auth.models import User, Group
from rest_framework import serializers
from manager.models import Students


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        

class StudentsSerializer(serializers.HyperlinkedModelSerializer):
    class_attended_field = serializers.CharField(source='class_attended')
    
    class Meta:
        model = Students
        fields = ['url', 'first_name', 'last_name', 'class_attended_field']