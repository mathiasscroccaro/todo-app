from todolist.serializers import TaskSerializer
from todolist.models import Task

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from todolist.permissions import IsTaskOwner


class TasksView(APIView):
    permission_classes = [IsTaskOwner]

    def get(self, request, format=None):
        tasks = Task.objects.all().filter(author=self.request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
