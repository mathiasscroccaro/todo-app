from django.contrib.auth.models import User, Group
from todolist.models import TodoItem
from rest_framework import viewsets
from todolist.api.serializers import UserSerializer, GroupSerializer, TodoItemSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)


class TodoItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TodoItems to be viewed or edited.
    """
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = (IsAuthenticated,)
