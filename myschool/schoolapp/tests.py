from os import name
from django.http import response
from django.test import TestCase, Client, tag
from .models import *
from .apis import *
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


# Create your tests here.

@tag('user')
class UserTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        User.objects.create(username='new_user')
    
    @tag('get_user')
    def test_get_user(self):
        response = self.client.get('/api/v1/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    @tag('create_user')
    def test_create_user(self):
        data = {
            'act': 'create',
            'detail': {
                'username': 'AAA',
                'password': '123'
            }
        }
        response = self.client.post('/api/v1/user/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'create success')
    
    @tag('duplicate_create_user')
    def test_duplicate_create_user(self):
        obj = User.objects.create(username='user A', password='1234')

        detail = {
            'username': 'user A',
            'password': '1234'
        }
        data = {
            'act': 'create',
            'detail': detail
        }
        response = self.client.post('/api/v1/user/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('update_user')
    def test_update_user(self):
        obj = User.objects.create(username='user A', password='1234')
        #to use the object above, we need to make a line that check whether it's still exists

        detail = {
            'username': 'B',
            'password': '1212'
        }
        data = {
            'act': 'update',
            # 'old username': str(obj.username),
            'detail': detail
        }
        response = self.client.post('/api/v1/user/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

    
    @tag('duplicate_update_user')
    def test_duplicate_update_user(self):
        obj = User.objects.create(username='user A', password='1234')

        detail = {
            'username': 'user A',
            'password': '1234'
        }
        data = {
            'act': 'update',
            'old name': str(obj.username),
            'detail': detail
        }
        response = self.client.post('/api/v1/user/', data, format='json')
        self.assertEqual(response.status_code, 400)

    @tag('delete_user')
    def test_delete_user(self):
        obj = User.objects.create(username='user 1', password='123')

        detail = {
            'username': 'user 1',
            'password': '123'
        }
        data = {
            'act': 'delete',
            'detail': detail
        }

        delete_user = obj.delete()

        response = self.client.post('/api/v1/user/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'delete success')

        users = User.objects.filter(
            username=data['detail']['username'], 
            password=data['detail']['password'])
        self.assertEqual(len(users), 0)
    
    @tag('missing_act_user')
    def test_missing_act_user(self):
        data = {
            'detail': {
                'username': 'user 1',
                'password': '123'
            }
        }

        response = self.client.post('/api/v1/user/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, act is required')


@tag('school')
class BasicTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
       
        #setup new school
        # School.objects.create(
        #     name = 'A',
        #     description = 'description A',
        #     user=self.new_user
        # )

    # no test function so the program will never run this one 
    # def get_area(self, w, h):
    #     area = w * h
    #     return area

    @tag('school_create_detail')
    def test_school_create_detail(self):
        data = {
            'act':'create',
            'detail': []
        }

        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['detail'] != dict)

    @tag('create_school')
    def test_create_school(self):
        data = {
            'act': 'create',
            'detail': {
                'name': 'AG',
                'description': 'AA'
            }
        }
        response = self.client.post('/api/v1/school/', data, format='json')
        # print('-------------------------', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'create success')

        schools = School.objects.filter(name=data['detail']['name'], description=data['detail']['description'], user=self.new_user)
        # print('---------------------', schools.first().user)
        # user__username='test'
        self.assertEqual(len(schools), 1)
    
    @tag('create_school_name')
    def test_create_school_name(self):
        data = {
            'act': 'create',
            'detail': {
                'name': 'school A'
            }
        }

        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'create success')

        school = School.objects.filter(name=data['detail']['name'], user=self.new_user)
        self.assertEqual(len(school), 1)
        self.assertTrue(school.first().name == 'school A')

    @tag('get_school')
    def test_get_school(self):
        # area = self.get_area(20, 40)
        response = self.client.get('/api/v1/school/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
    
    #test update school
    @tag('update_school')
    def test_update_school(self):
        obj = School.objects.create(name='A', description='description A', user=self.new_user)
        
        detail = {
            'school_pk': str(obj.pk),
            'name':'G',
            'description': 'description G'
        }

        data = {
            'act':'update',
            'detail':detail
            }
        print('---------------------ss', data)
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        # temp
        objs = School.objects.filter(user=self.new_user)

        # check new name of updated school
        updated_objs = School.objects.filter(user=self.new_user, name='G', pk=data['detail']['school_pk'])
        self.assertEqual(len(updated_objs), 1)

        # check old school
        objs = School.objects.filter(user=self.new_user, name='A')
        self.assertEqual(len(objs), 0)
    
    @tag('update_school_name')
    def test_update_school_name(self):
        School.objects.create(
            name='A',
            description='description A',
            user=self.new_user,
        )

        detail = {
            'name': 'B',
        }

        data = {
            'act': 'update',
            'detail': detail
        }
        
        response = self.client.post('/api/v1/school/', data, format='json')
        print('===================1', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        # objs = School.objects.filter(user=self.new_user)

        new_name = School.objects.filter(name=detail['name'], user=self.new_user)
        self.assertEqual(len(new_name), 1)
        self.assertTrue(new_name.first().name == detail['name'])

        objs = School.objects.filter(name='A', user=self.new_user)
        self.assertEqual(len(objs), 0)
    
    @tag('update_school_description')
    def test_update_school_description(self):
        School.objects.create(
            name='A',
            description='this is school',
            user=self.new_user)
        
        detail = {
            'description': 'new school description'
        }

        data = {
            'act': 'update',
            'detail': detail
        }

        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        new_description = School.objects.filter(description=detail['description'], user=self.new_user)
        self.assertEqual(len(new_description), 1)
        # we can do as what below or we can just use 'assertTrue' so that we don't need 'True' at the end.
        self.assertEqual(new_description.first().description == detail['description'], True)

        old_description = School.objects.filter(description='this is school', user=self.new_user)
        self.assertEqual(len(old_description), 0)

    @tag('duplicate_update_school')
    def test_update_duplicate_school(self):
        School.objects.create(name="A", description='description A', user=self.new_user)
        
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
    
    @tag('duplicate_create_school')
    def test_create_duplicate_school(self):
        obj = School.objects.create(
            user=self.new_user, 
            name='school A', 
            description='description A')
        
        detail = {
            'name': 'school A',
            'description': 'dedesciptiopn A'
        }
        data = {
            'act':'create',
            'detail': detail
        }
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 400)

    @tag('delete_school')
    def test_delete_school(self):
        obj = School.objects.create(name='school A', description='123', user=self.new_user)

        detail = {
            'school_pk': str(obj.pk),
        }
        data = {
            'act': 'delete',
            'detail': detail
        }
        print('----------------d', data)
        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'delete success')

        schools = School.objects.filter(pk=data['detail']['school_pk'])
        self.assertEqual(len(schools), 0)

    @tag('missing_act_school')
    def test_missing_act_school(self):
        data = {
            'detail': {
                'name': 'school A',
                'description': '123'
            }
        }

        response = self.client.post('/api/v1/school/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, act is required')

@tag('grade')
class GradeTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.school = School.objects.create(user=self.new_user, name='school A', description='description A')
       
        #setup new grade
        # Grade.objects.create(
        #     name = '1',
        #     description = 'description 1'
        # )
    
    @tag('create_grade')
    def test_create_grade(self):
        data = {
            'act': 'create',
            'detail': [
                {
                    "name": "grade 1",
                    "description": "this is description for grade 1"
                },
                {
                    "name": "grade 2",
                },
                {
                    "name": "grade 3",
                    "description": "this is description for grade 3"
                }
            ]
        }
        # print('--------------------ss', data['detail'])

        print('-------------------------------ww', data)
        response = self.client.post('/api/v1/grade/', data, format='json')
        print('------------------------aaa', response.data)
        self.assertEqual(response.status_code, 200)
        # print('------------------------------------')
        self.assertEqual(response.data, 'create %d success'%len(data['detail']))

        grades = Grade.objects.all() #since we let the user create list, we have to check every queryset as it of the user.

        # print('------------------------------aaaa', grades)
        self.assertEqual(len(grades), 3)

    # @tag('create_grade_name')
    # def test_create_grade_name(self):
    #     data = {
    #         'act': 'create',
    #         'detail': [
    #             {
    #                 "name": "grade 1",
    #             },
    #             {
    #                 "name": "grade 2",
    #             },
    #             {
    #                 "name": "grade 3",
    #             }
    #         ]
    #     }
    #     response = self.client.post('/api/v1/grade/', data, format='json')
    #     print('--------------------aaa', response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, 'create success')

    #     grade_name = Grade.objects.filter(name=data['detail'])
    #     self.assertEqual(len(grade_name), 3)
    # @tag('create_grade')
    # def test_create_grade(self):
    #     grade_name = []
    #     for i in ['m1', 'm2', 'm3']:
    #         gradeses = Grade.objects.create(
    #             name=i,
    #             school=self.school
    #         )
    #         grade_name.append(gradeses)

    #     check_g = Grade.objects.all()
    #     self.assertTrue(len(check_g), 3) 

    #     data = {
    #         'act': 'create',
    #         'detail': {
    #             'name': grade_name,
    #             'description': 'description 1'
    #         }
    #     }
    #     response = self.client.post('/api/v1/grade/', data, format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, 'create success')

        # grades = Grade.objects.filter(name=data['detail']['name'], description=data['detail']['description'], school=self.school)
        # # print('------------------------------aaaa', grades)
        # self.assertEqual(len(grades), 1)

    @tag('missing_act_grade')
    def test_missing_act(self):
        data = {
            'detail': {
                'name': '1',
                'description': 'description 1'
            }
        }
        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, act is required')

    @tag('get_grade')
    def test_get_grade(self):
        obj = []
        for name in ['a','b','c']:
            query_names = Grade.objects.create(name=name, school=self.school)
            obj.append(query_names)
        response = self.client.get('/api/v1/grade/')
        print('----------------------111', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
    
    @tag('duplicate_create_grade')
    def test_create_duplicate_grade(self):
        names = []
        for grade_name in ['1','2','3']:
            grade = Grade.objects.create(
                school=self.school,
                name=grade_name)
            names.append(grade)

        # print('-==========================dd', names)
        detail = [
                {
                    "name": "1",
                    "description": "this is description for grade 1"
                },
                {
                    "name": "2",
                    "description": "this is description for grade 2"
                },
                {
                    "name": "3",
                    "description": "this is description for grade 3"
                }
            ]
        # print('=======================66',detail)
        data = {
            'act':'create',
            'detail':detail
            }
        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('update_grade')
    def test_update_grade(self):
        names = []
        for grade_name in ['c1','c2','c3']:
            grade = Grade.objects.create(
                school=self.school,
                name=grade_name)
            names.append(grade.pk)
            # print('============',grade)

        detail = [
            {
                'pk': '1',
                'name': 'a',
                'description': 'd for a'
            },
            {
                'pk': '2',
                'name': 'b'
            },
            {
                'pk': '3',
                'name': 'c',
                'description': 'd for c'
            }
        ]
        data = {
            'act': 'update',
            'detail': detail
        }
        # print('-------------------------qq', detail[0]['name'], detail[1]['name'], detail[2]['name'])
        response = self.client.post('/api/v1/grade/', data, format='json')
        print('---------------------------dd',response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        #check updated grade
        name_list = [detail[0]['name'], detail[1]['name'], detail[2]['name']]
        print('--------------------ii',len(name_list))
        new_query_name = []
        for name in name_list:
            print('-----------------------------qwe', name)
            updated_objs = Grade.objects.filter(name=name,school=self.school)
            # updated_description = Grade.objects.filter(description=name, school=self.school)
            print('-----------------------uuu', updated_objs)
            # print('----------------------dddd', updated_description)
            new_query_name.append(updated_objs)
            # print('--------------------', len(new_query_name))
        self.assertEqual(len(new_query_name), 3)
        # self.assertEqual(len(updated_description), 1)

        #check old grade
        objs = Grade.objects.filter(name=grade_name, school=self.school)
        self.assertEqual(len(objs), 0)
    
    @tag('grade_update_description')

    @tag('update_grade_format')
    def test_update_grade_format(self):
        name = []
        for grade_name in ['c1','c2','c3']:
            grade = Grade.objects.create(
                name=grade_name,
                school=self.school)
            name.append(grade.pk)
        
        detail = [
            {
                'pk': '1',
                'name': 'a',
                'description': 'd for a'
            },
            {
                'pk': '2',
                'name': 'b'
            },
            {
                'pk': '3',
                'name': 'c',
                'descriptions': 'd for c'
            }
        ]

        data = {
            'act': 'update',
            'detail': detail
        }

        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'incorrect format')

    
    @tag('duplicate_update_grade')
    def test_duplicate_update_grade(self):
        names = []
        for grade_name in ['a','b','c']:
            grade = Grade.objects.create(
                school=self.school,
                name=grade_name)
            names.append(grade.pk)
            print('----------------------io', names)
        detail = [
            {
                'pk': '1',
                'name': 'a',
                'description': 'd for a'
            },
            {
                'pk': '2',
                'name': 'b',
                'description': 'd for b'
            },
            {
                'pk': '3',
                'name': 'c',
                'description': 'd for c'
            }
        ]
        data = {
            'act': 'update',
            'detail': detail
        }
        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('delete_grade')
    def test_delete_grade(self):
        obj = Grade.objects.create(name='A', description='123', school=self.school)

        detail = {
            'pk': str(obj.pk)
        }
        data = {
            'act': 'delete',
            'detail': detail
        }

        response = self.client.post('/api/v1/grade/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'delete success')

        grades = Grade.objects.filter(
            pk=data['detail']['pk'],
            school=self.school)
        self.assertEqual(len(grades), 0)
    

@tag('student')
class StudentTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.school = School.objects.create(user=self.new_user, name='school A')
        self.grade = Grade.objects.create(school=self.school)

        # Student.objects.create(
        #     first_name='F1',
        #     last_name='L1',
        #     nick_name='N1')
    
    @tag('create_student')
    def test_create_student(self):
        data = {
            'act': 'create',
            'detail': {
                'grade': str(self.grade.pk),
                'first_name': 'N1',
                'last_name': 'N2',
                'nick_name': 'N3'
            }
        }
        print('-----------------------ie', data)
        response = self.client.post('/api/v1/student/', data, format='json')
        print('----------------------------rr', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'create success')

        students = Student.objects.filter(
            first_name=data['detail']['first_name'], 
            last_name=data['detail']['last_name'], 
            nick_name=data['detail']['nick_name'],
            grade=self.grade)
        print(students)
        self.assertEqual(len(students), 1)
    
    @tag('get_student')
    def test_get_student(self):
        response = self.client.get('/api/v1/student/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
    
    @tag('duplicate_create_student')
    def test_create_duplicate_student(self):
        obj = Student.objects.create(
            first_name='F1',
            last_name='L1',
            nick_name='N1',
            grade=self.grade
        )
        data = {
            'act': 'create',
            'detail': {
                'grade': str(self.grade.pk),
                'first_name':'F1',
                'last_name': 'L1',
                'nick_name': 'N1'
            }
        }
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('update_student')
    def test_update_student(self):
        obj = Student.objects.create(
            first_name='F1',
            last_name='L1',
            nick_name='N1',
            grade = self.grade
        )

        detail = {
            'student_pk': str(obj.pk),
            'first_name':'F2',
            'last_name': 'L2',
            'nick_name': 'N2'
        }
        data = {
            'act': 'update',
            'detail': detail
        }
        print('---------------------44', data)
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 200)
        print('---------------------123', data)
        self.assertEqual(response.data, 'update success')


        updated_objs = Student.objects.filter(pk=obj.pk, first_name='F2', last_name='L2', nick_name='N2')
        self.assertEqual(len(updated_objs), 1)

        objs = Student.objects.filter(pk=obj.pk, first_name='F1', last_name='L1', nick_name='N1')
        self.assertEqual(len(objs), 0)

    @tag('duplicate_update_student')
    def test_duplicate_update_student(self):
        obj = Student.objects.create(
            first_name='F1',
            last_name='L1',
            nick_name='N1',
            grade = self.grade
        )

        detail = {
            'student_pk': str(obj.pk),
            'first_name': 'F1',
            'last_name': 'L1',
            'nick_name': 'N1'
        }
        data = {
            'act': 'update',
            'detail': detail
        }
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('delete_student')
    def test_delete_student(self):
        obj = Student.objects.create(
            first_name='F1',
            last_name='L1',
            nick_name='N1',
            grade = self.grade)

        detail = {
            'student_pk': str(obj.pk)
        }
        data = {
            'act': 'delete',
            'detail': detail
        }
        print('------------------------qqq', detail)
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'delete success')

        grades = Student.objects.filter(
            pk=data['detail']['student_pk'],
            grade=self.grade)
        print(grades)
        self.assertEqual(len(grades), 0)

    @tag('missing_act_student')
    def test_missing_act(self):
        data = {
            'detail': {
                'first_name':'F1',
                'last_name': 'L1',
                'nick_name': 'N1'
            }
        }
        response = self.client.post('/api/v1/student/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, act is required')


@tag('parent')
class ParentTest(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        self.school = School.objects.create(
        name='school A',
        description='description A',
        user=self.new_user
        )
        self.grade = Grade.objects.create(
            name='1',
            description='description 1',
            school=self.school
        )
        self.child = Student.objects.create(
            first_name='F1',
            last_name='L1',
            nick_name='N1',
            grade = self.grade
        )
        # Parent.objects.create(
        #     first_name='P1',
        #     last_name='L1'
        # )
    
    @tag('get_parent')
    def test_get_parent(self):
        response = self.client.get('/api/v1/parent/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
    
    @tag('create_parent')
    def test_create_parent(self):
        data = {
            'act': 'create',
            'detail': {
                'first_name': 'P1',
                'last_name': 'L1',
                # 'children': str(self.children)
            }
        }
        
        # p1 = data.children.add(self.children)
        
        response = self.client.post('/api/v1/parent/', data, format='json')
        print('------------------------33', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'create success')

        parents = Parent.objects.filter(
            first_name=data['detail']['first_name'], 
            last_name=data['detail']['last_name'],
            director=self.new_user,
            )
        print('----------------------------111',)
        self.assertEqual(len(parents), 1)

    @tag('duplicate_create_parent')
    def test_duplicate_create_parent(self):
        obj = Parent.objects.create(
            first_name='P1',
            last_name='L1',
            director=self.new_user,
        )

        detail = {
            'first_name': 'P1',
            'last_name': 'L1'
        }
        data = {
            'act': 'create',
            'detail': detail
        }
        response = self.client.post('/api/v1/parent/', data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @tag('update_parent')
    def test_update_parent(self):
        obj = Parent.objects.create(
            first_name='P1',
            last_name='L1',
            director=self.new_user,
        )
        
        detail = {
            'parent_pk': str(obj.pk),
            'first_name': 'P2',
            'last_name': 'L2'
        }
        data = {
            'act': 'update',
            'detail': detail
        }
        response = self.client.post('/api/v1/parent/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'update success')

        update_objs = Parent.objects.filter(pk=obj.pk, first_name='P2', last_name='L2')
        self.assertEqual(len(update_objs), 1)

        objs = Parent.objects.filter(pk=obj.pk, first_name='P1', last_name='L1' )
        self.assertEqual(len(objs), 0)

    @tag('duplicate_update_parent')
    def test_duplicate_update_parent(self):
        obj = Parent.objects.create(
            first_name='P1',
            last_name='L1',
            director=self.new_user
        )

        obj.children.add(self.child)

        detail = {
            'parent_pk': str(obj.pk), 
            # need 'pk' since in [api] still not yet reach the process of updating the object 
            # --> at this point we just check the duplicated parent
            'first_name': 'P1',
            'last_name': 'L1'
        }
        data = {
            'act': 'update',
            'detail': detail
        }
        response = self.client.post('/api/v1/parent/', data, format='json')
        self.assertEqual(response.status_code, 400)

    @tag('delete_parent')
    def test_delete_parent(self):
        obj = Parent.objects.create(
            first_name='F1',
            last_name='L1',
            director=self.new_user)
        
        print('=======================45', obj)

        detail = {
            'parent_pk': str(obj.pk)
        }
        data = {
            'act': 'delete',
            'detail': detail
        }

        # obj.delete() --> if we put this here, in the test, it will delete the queryset before it goes to the api, then that will result in failure 400

        response = self.client.post('/api/v1/parent/', data, format='json')
        # print('--------------------------11',response.data )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'delete success')

        parents = Parent.objects.filter(
            pk=data['detail']['parent_pk'],
            director=self.new_user)
        self.assertEqual(len(parents), 0)

    # @tag('add_children')
    # def test_add_children(self):
    #     obj = Parent.objects.create(
    #         first_name='F1',
    #         last_name='L1',
    #         director=self.new_user)

    #     data = {
    #         'act': 'add children',
    #         'parent': str(obj.pk),
    #         'children': str(self.child.pk)
    #     }
    #     response = self.client.post('/api/v1/parent/', data, format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, 'children added')

    #     parents = Parent.objects.filter(pk=obj.pk, director=self.new_user)
    #     self.assertEqual(len(parents), 1)

    #     # check whether there is a child in parent --> the child must be correct according to the parent's input 
    #     parent = parents.first()
    #     children = parent.children.all()
    #     child = children.filter(pk=data['children'])
    #     self.assertEqual(len(child), 1)
    @tag('add_children')
    def test_add_children(self):
        # setup
        parent = Parent.objects.create(
            director = self.new_user,
            first_name = 'john',
        )
        children = []
        for name in ['sam1', 'sam2', 'sam3', 'sam4', 'sam5']:
            child = Student.objects.create(
                grade = self.grade,
                first_name = name,
            )
            children.append(child)
        print('-------------------vv', children)
        _ = Parent.objects.all()
        self.assertTrue(len(_) >= 1)
        _ = Student.objects.all()
        self.assertTrue(len(_) >= 5)

        # '''
        # create list_children_pk
        # [
        #     {
        #         'pk': '1'
        #     },

        #     {
        #         'pk': '3'
        #     },

        #     {
        #         'pk': '5'
        #     }
        # ]
        # '''
        children_pk = []
        for child in children[:2]:
            _ = {
                'pk': str(child.pk)
            }
            children_pk.append(_)
        
        detail = {
            'parent_pk' : str(parent.pk),
            'children_pk': children_pk,
        }

        # post data
        data = {
            'act': 'add children',
            'detail': detail
        }
        # print('===========================sdsd', data['children_pk'])
        response = self.client.post('/api/v1/parent/', data, format='json')
        # print('=-============================rr', response.data)
        self.assertTrue(response.status_code == 200)

        # check children in parent
        parent = Parent.objects.get(pk=data['detail']['parent_pk'])
        children = parent.children.all()
        self.assertTrue(len(children) == 2)
        self.assertTrue(children[0].first_name == 'sam1')
        self.assertTrue(children[1].first_name == 'sam2')

    @tag('missing_act_parent')
    def test_missing_act(self):
        data = {
            'detail': {
                'first_name': 'P1',
                'last_name': 'L2'
            }
        }
        response = self.client.post('/api/v1/parent/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'failed, action is required')
    
    
