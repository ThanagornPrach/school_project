from django.http import response
from django.test import TestCase, Client
from .models import *
from .apis import *

# Create your tests here.

class BasicTest(TestCase):
    def setUp(self):
        self.client = Client()

        #setup new school
        School.objects.create(
            school = 'A'
        )
    def test_get_school(self):
        response = self.client.get('/api/v1/test1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'success')
    
    def test_create_duplicate_school(self):
        data = {
            'act':'create',
            'detail':{
                'school':'A'
            }
        }
        response = self.client.post('/api/v1/test1/', data, format='json')
        self.assertEqual(response.status_code, 400)

class GradeTest(TestCase):
    def setUp(self):
        self.client = Client()
        Grade.objects.create(
            grade = '1'
        )
    
    def test_get_grade(self):
        response = self.client.get('/api/v1/test2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'success')