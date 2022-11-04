from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from API.serializers import UserSerializer, GroupSerializer, StudentsSerializer
from manager.models import Students


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    

class StudentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited.
    """
    queryset = Students.objects.all().order_by('last_name')
    serializer_class = StudentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']