from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import datetime


class APITestGetDefault(TestCase):
    fixtures = ['default_user.json', 'default_todo_item.json']
    
    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

        response = self.client.post(
            '/token', {
                'username': 'mathias',
                'password': 'mathias'
            }
        )
        self.token = response.json()['access']

    def test_get_todoitems(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        res = client.get('/todo_items/').json()
        
        expected = [{
            'id': 1, 
            'post': {
                'title': 'default todo item', 
                'details': ['todo 1', 'todo 2']
            }, 
            'created_at': '2022-05-03T21:54:24.691202Z', 
            'author': 1}]

        self.assertEqual(expected, res)

    def test_create_todoitem(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        timestamp = datetime.datetime.now().isoformat()

        data = {
            'author': 1,
            'created_at': timestamp,
            'post': {
                'title': 'another item'
            }
        }
        
        expected = data['post']

        client.post('/todo_items/',  data, 'json')
        res = client.get('/todo_items/').json()
        res = res[1]['post']
       
        self.assertEqual(expected, res)
    
    def test_delete_todoitem(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {
            'author': 1,
            'post': {
                'title': 'another second item'
            }
        }
        
        client.post('/todo_items/',  data, 'json')

        expected = data['post']
        client.delete('/todo_items/1/')
        res = client.get('/todo_items/2/').json()['post']
       
        self.assertEqual(expected, res)
    
    def test_patch_todoitem(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {
            'post': {
                'title': 'another modified item'
            }
        }
        expected = data['post']
        
        client.patch('/todo_items/1/',  data, 'json')

        res = client.get('/todo_items/1/').json()['post']
       
        self.assertEqual(expected, res)
