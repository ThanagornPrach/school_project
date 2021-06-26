from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.http import response
from django.test import TestCase, Client, tag
from .models import *
from .apis import *
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token


# Create your tests here.
class BasicTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
       
        #setup new school
        School.objects.create(
            name = 'A',
            description = 'description A'
        )

    # no test function so the program will never run this one 
    # def get_area(self, w, h):
    #     area = w * h
    #     return area

    @tag('missing_act')
    def test_missing_act(self):
        data = {
            'detail': {
                'name': 'A',
                'description': 'description A'
            }
        }
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, action is required')

    @tag('get')
    def test_get_school(self):
        # area = self.get_area(20, 40)
        response = self.client.get('/api/v1/school/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'success')
    
    #test update school
    @tag('update')
    def test_update_school(self):
        obj = School.objects.create(name='A', description='description A', user=self.new_user)
        
        detail = {
            'name':'G',
            'description': 'description G'
        }

        data = {
            'act':'update',
            # 'pk':str(obj.pk), 
            'detail':detail
            }
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        # temp
        objs = School.objects.filter(user=self.new_user)

        # check new name of updated school
        updated_objs = School.objects.filter(user=self.new_user, name='G')
        self.assertEqual(len(updated_objs), 1)

        # check old school
        objs = School.objects.filter(user=self.new_user, name='A')
        self.assertEqual(len(objs), 0)

    @tag('duplicate_update')
    def test_update_duplicate_school(self):
        obj = School.objects.create(name="A", description='description A', user=self.new_user)
        
        detail = {
            'name': 'A',
            'description': 'description A'
        }
        data = {
            'act': 'update',
            'detail': detail
        }
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 400)

        # should we also have this one here?
        # objs = School.objects.filter(user=self.new_user)

    # @tag('missing_update')
    # def test_update_missing_act(self):
    #     data = {
    #         # 'act':'update',
    #         'detail': 'detail'
    #     }
    #     response = self.client.post('/api/v1/school/', data, format='json')
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.data, 'failed, action is required')
    
    @tag('duplicate_create')
    def test_create_duplicate_school(self):
        data = {
            'act':'create',
            'detail':{
                'name':'A',
                'description': 'description A'

            }
        }
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 400)

@tag('grade')
class GradeTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
       
        #setup new grade
        Grade.objects.create(
            name = '1',
            description = 'description 1'
        )
    
    @tag('missing_act')
    def test_missing_act(self):
        data = {
            'detail': {
                'name': '1',
                'description': 'description 1'
            }
        }
        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, action is required')

    @tag('get')
    def test_get_grade(self):
        response = self.client.get('/api/v1/grade/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'success')
    
    @tag('duplicate_create')
    def test_create_duplicate_grade(self):
        data = {
            'act':'create',
            'detail':{
                'name':'1',
                'description': 'description 1'
            }
        }
        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('update')
    def test_update_grade(self):
        obj = Grade.objects.create(name='1', description="description 1", user=self.new_user)

        detail = {
            'name': '2',
            'description': 'description 2'
        }
        data = {
            'act': 'update',
            'detail': detail
        }
        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        objs = Grade.objects.filter(user=self.new_user)

        #check updated grade
        updated_objs = Grade.objects.filter(user=self.new_user, name='2')
        self.assertEqual(len(updated_objs), 1)

        #check old grade
        objs = Grade.objects.filter(user=self.new_user, name='1')
        self.assertEqual(len(objs), 0)

@tag('student')
class StudentTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.school = School.objects.create(user=self.new_user, name='school A')

        self.grade = Grade.objects.create(school=self.school)
    
    @tag('get')
    def test_get_student(self):
        response = self.client.get('/api/v1/student/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'success')
    
    @tag('duplicate_create')
    def test_create_duplicate_student(self):
        data = {
            'act': 'create',
            'detail': {
                'first_name':'F1',
                'last_name': 'L1',
                'nick_name': 'N1'
            }
        }
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('missing_act')
    def test_missing_act(self):
        data = {
            'detail': {
                'first_name':'F1',
                'last_name': 'L1',
                'nick_name': 'N1'
            }
        }
        response = self.client.post('/api/v1/student', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, action is requited')
    
    @tag('update_student')
    def test_update_student(self):
        obj = Student.objects.create(
            first_name='F1',
            last_name='L1',
            nick_name='N1',
            grade = self.grade
        )

        detail = {
            'first_name':'F2',
            'last_name': 'L2',
            'nick_name': 'N2'
        }
        data = {
            'act': 'update',
            'pk':str(obj.pk),
            'detail': detail
        }
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')


        updated_objs = Student.objects.filter(
            pk=obj.pk, first_name='F2', last_name='L2', nick_name='N2')
        self.assertEqual(len(updated_objs), 1)

        objs = Student.objects.filter(pk=obj.pk, first_name='F1', last_name='L1', nick_name='N1')
        self.assertEqual(len(objs), 0)
