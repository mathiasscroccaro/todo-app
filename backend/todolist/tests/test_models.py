from django.test import TestCase

from todolist.models import Task
from django.contrib.auth.models import User

from todolist.serializers import TaskSerializer


class TestTask(TestCase):
    def test_create_task(self): 
        user = User(
            username='Mathias',
            password='Mathias'
        )
        user.save()

        parent_task_title = 'Go to the market'
        child_task_title = 'Buy rice'

        parent_task_model = Task(
            author=user,
            title=parent_task_title
        )
        parent_task_model.save()

        child_task_model = Task(
            title=child_task_title,
            parent_task=parent_task_model
        )
        child_task_model.save()

        task_parent_item = Task.objects.first()

        self.assertEqual(task_parent_item.author, user) 
        self.assertEqual(task_parent_item.title, parent_task_title) 
        self.assertEqual(task_parent_item.children_tasks.all()[0].title, 'Buy rice') 

    def test_create_model_serialized(self):
        user = User(
            username='Mathias',
            password='Mathias'
        )
        user.save()
        
        parent_data = {
            'title': 'Go to the market',
            'author': 1
        }
        serializer = TaskSerializer(data=parent_data)
        serializer.is_valid()
        serializer.save()

        task_item = Task.objects.first()
        self.assertEqual(task_item.title, parent_data['title'])
        self.assertEqual(task_item.author, user)

        child_data = {
            'parent_task': 1,
            'title': 'Buy rice',
            'author': 1
        }
        serializer = TaskSerializer(data=child_data)
        serializer.is_valid()
        serializer.save()

        task_item = Task.objects.get(title='Buy rice')
        self.assertEqual(task_item.title, child_data['title'])
