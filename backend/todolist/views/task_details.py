from todolist.serializers import TaskSerializer
from todolist.models import Task

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from todolist.permissions import IsTaskOwner


class TaskDetailsView(APIView):
    permission_classes = [IsTaskOwner]

    def get_object(self, id):
        try:
            return Task.objects.get(pk=id)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, task_id, format=None):
        task = self.get_object(task_id)
        # Will call IsTaskOwner.has_object_permission
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, task_id, format=None):
        task = self.get_object(task_id)
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, format=None):
        task = self.get_object(task_id)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
