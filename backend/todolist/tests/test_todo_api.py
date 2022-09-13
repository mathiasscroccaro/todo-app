from django.test import TestCase
from django.contrib.auth.models import User


class TestTask(TestCase):
    # Default data populated in the test DB and used in the tests set
    fixtures = ['default_user.json', 'default_tasks.json']

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

        # Default logged user for the tests
        self.client.post(
            '/login/', {
                'username': 'mathias',
                'password': 'mathias'
            }
        )

    def test_wrong_credentials(self):
        response = self.client.post(
            '/login/', {
                'username': 'mathias',
                'password': '123'
            }
        )
        self.assertEqual(response.status_code, 401)
    
    def test_get_todolist(self):
        tasks = self.client.get('/tasks/').json()
        subtasks = tasks[0].get('children_tasks', None)

        self.assertEqual(tasks[0].get('title'), 'Go to the market')
        self.assertEqual(subtasks[0].get('title', None), 'Buy an underwear')

    def test_get_todolist_without_loggin(self):
        self.client.post('/logout/')
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 403)
    
    def test_post_todolist_logged_with_different_user(self):
        self.client.post(
            '/login/', {
                'username': 'dummy',
                'password': 'dummy'
            }
        )

        self.client.post('/tasks/', {
            'title': 'Go to the mall',
        })
        
        response = self.client.get('/tasks/')
        tasks = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tasks[0]['author'], 2)
        self.assertEqual(tasks[0]['title'], 'Go to the mall')

        response = self.client.get('/tasks/1/')
        self.assertEqual(response.status_code, 403)
        
    def test_get_task_by_id(self):
        task = self.client.get('/tasks/1/').json()
        self.assertEqual(task.get('title'), 'Go to the market')

    def test_get_task_by_wrong_id(self):
        response = self.client.get('/tasks/666/')
        self.assertEqual(response.status_code, 404)
    
    def test_update_task_by_id(self):
        self.client.post('/tasks/', {
            'title': 'Buy a sweety'
        })

        self.client.patch(
            '/tasks/3/', 
            {
                'created_at': '2022-05-03T21:54:24.691202Z',
                'parent_task': 1               
            }, 
            content_type='application/json'
        ).json()

        task = self.client.get('/tasks/1/').json()
        subtask = task['children_tasks'][1]

        self.assertEqual(task['title'], 'Go to the market')
        self.assertEqual(subtask['title'], 'Buy a sweety')
    
    def test_update_task_by_wrong_id(self):
        response = self.client.patch('/tasks/666/')
        self.assertEqual(response.status_code, 404)

    def test_delete_task_by_id(self):
        self.client.delete('/tasks/1/')
        response = self.client.get('/tasks/')
        self.assertEqual(response.json(), [])

    def test_delete_task_by_wrong_id(self):
        response = self.client.delete('/tasks/666/')
        self.assertEqual(response.status_code, 404) 
