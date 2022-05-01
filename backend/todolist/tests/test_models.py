from django.test import TestCase
from todolist.models import TodoItem
from django.contrib.auth.models import User
from todolist.api.serializers import TodoItemSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

import datetime
import io


class TestTodoItem(TestCase):
    def test_create_model(self):
        user = User(
            username='Mathias',
            password='Mathias'
        )
        user.save()

        post = {
            'title': 'Do english homework',
            'details': [
                {
                    'task': 'To Write about my experience',
                    'done': False
                },
                {
                    'task': 'To do something nice',
                    'done': True
                }
            ]
        }
        model = TodoItem(
            author=user,
            post=post
        )
        model.save()
        todo_item = TodoItem.objects.first()

        self.assertEqual(todo_item.post, post)
        self.assertEqual(todo_item.author, user)

    def test_create_model_serialized_with_example(self):
        user = User(
            username='Mathias',
            password='Mathias'
        )
        user.save()

        todoitem = TodoItem(
            author=user,
            post={'title': 'trying to serialize'}
        )

        serializer = TodoItemSerializer(todoitem)

        json = JSONRenderer().render(serializer.data)

        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)

        serializer = TodoItemSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        
        expected_post = {'title': 'trying to serialize'}

        todo_item = TodoItem.objects.first()
        self.assertEqual(todo_item.post, expected_post)
        self.assertEqual(todo_item.author, user)

    def test_create_model_serialized(self):
        user = User(
            username='Mathias',
            password='Mathias'
        )
        user.save()
        
        data = {
            'post': {'title': 'My second test'},
            'author':1
        }
        serializer = TodoItemSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        todo_item = TodoItem.objects.first()
        self.assertEqual(todo_item.post, data['post'])
        self.assertEqual(todo_item.author, user)
