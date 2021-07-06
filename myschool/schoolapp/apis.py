from django.http import response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

class APIUser(APIView):
    def get(self, request):
        data = request.GET.dict()
        this_user = request.user
        objs = User.objects.filter(username=this_user)
        obj = objs.first()
        serializer = UserSerializer(obj, many=False)
        return Response(serializer.data, status=200)
    
    def post(self, request): 
        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            username = detail['username']
            objs = User.objects.filter(username=username)
            if objs.exists():
                return Response('duplicated username', status=400)

            new_user = User.objects.create_user(username=detail['username'], password=detail['password'])
            new_user.save()
            # serialzer = UserSerializer(data=detail, many=False)
            # if serialzer.is_valid():
            #     serialzer.save()
            return Response('create success', status=200)
            # else:
            #     return Response(serialzer.errors, status=400) 

            # new_user = User.objects.create_user(username='username', password='password')
            # new_user.save()
            # return Response('create success', status=200)
        
        if act == 'update':
            this_user = request.user
            users = User.objects.filter(username=this_user)
           
            username = detail['username']
            objs = User.objects.filter(username=username)
            if objs.exists():
                return Response('duplicated update', status=400)
            
            if not users.exists():
                return Response('unable to update', status=400)
            
            users.update(**data['detail'])
            return Response('update success', status=200)
        
        if act == 'delete':
            this_user = request.user
            delete_user = User.objects.filter(username=this_user).delete()
            return Response('delete success', status=200)
        else:
            return Response('unable to delete', status=400)



class APISchool(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        data = request.GET.dict()
        this_user = request.user
        # print('---------------------', this_user.pk)

        objs = School.objects.filter(user=this_user)
        # print('-------------------------', objs)
        # print('len all objs in this user', len(objs))
        # abcs = objs.filter(name='abc')
        # print('len abc in this user', len(abcs))

        obj = objs.first()
        # ans = obj.name
        # print('description of schools=', ans)

        # obj = objs.first()
        serializer = SchoolSerializer(obj, many=False)
        return Response(serializer.data, status=200)

    def post(self, request):
        # user = User.objects.get(username='P')
        # token_of_p = Token.objects.get(user = user)
        # token_ = 'Token 00084e7ffe28f841c749cf6b4f957176070bd4a9 '
        # print('token of P=', token_of_p.key == token_)
        # print(request.user, '------aaa')
        # 12/0
        data = request.data
        act = data.get('act')
        detail = data.get('detail')

        if act == 'create':
            detail.update({
                'user':request.user.pk
            })
            name = detail['name']
            objs = School.objects.filter(name=name)
            if objs.exists():
                return Response ('duplicated school', status=400)

            print('------------------------sssss', detail)
            serializer = SchoolSerializer(data=detail, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response('create success', status=200)
            else:
                return Response(serializer.errors, status=400)

        if act == 'update':
            # get school of this user
            this_user = request.user
            schools = School.objects.filter(user=this_user)
            # print('--------------------------ans',School.objects.filter(user=this_user))
            name = detail['name']
            objs = School.objects.filter(name=name)
            if objs.exists():
                return Response('duplicated school', 400)


            if not schools.exists():
                return Response('fail', status=400)

            # # approach 1 - single update
            # # get new school name from user
            # new_code = request.data['detail']['school']
            # obj = schools[0]
            # obj.school = new_code
            # obj.save()

            # # approach 2 - multi update #update all schools(object) that the user requested
            schools.update(**request.data['detail'])

            # schools = <QuerySet>[obj1, obj2, obj3]
            # obj1.code = 'oldcode'
            # obj1.name = 'b1'
            # obj1.province = 'p1'

            # obj2.code = 'code2'
            # obj2.name = 'b2'
            # obj2.province = 'p2'

            # detail = {
            #     'code': 'newcode',
            #     'name': 'newname',
            #     'province': 'new',
            # }

            return Response('update success', status=200)
        
        if act == 'delete':
            this_user = request.user
            schools = School.objects.filter(user=request.user)
            delete_school = schools.delete()
            if not schools.exists():
                return Response('delete success', status=200)
            else:
                return Response('unable to delete', status=400)

        return Response('failed, action is required', status=400)     

# class APIAllStudent(APIView):
#     model = Student
#     serializer = StudentOnlyNameSerializer
#     def get(self, request):
#         objs = self.model.objects.all()
#         ser = self.serializer(objs, many=True)
#         return Response(ser.data, status=200)

# class APIAllSchoolDescription(APIView):
#     model = School
#     serializer = SchoolOnlyDescriptionSerializer
#     def get(self, request):
#         objs = self.model.objects.all()
#         ser = self.serializer(objs, many=True)
#         return Response(ser.data, status=200)

class APIGrade(APIView):
    def get(self, request):
        data = request.GET.dict()
        objs = Grade.objects.filter(school__user=request.user)
        # print('-------------------------', objs)
        obj = objs.first()

        # print('------------------------result', objs)

        # # ver1
        # for obj in objs:
        #     school_pk = obj.school.pk
        #     school_obj = School.objects.get(pk=school_pk)
        #     obj.school_name = school_obj.name

        # # ver2
        # obj = objs.first()
        # school_pk = obj.school.pk
        # school_obj = School.objects.get(pk=school_pk)

        # for obj in objs:
        #     obj.school_name = school_obj.name
        serializer = GradeSerializer(obj, many=False)
        # data_out = serializer.data
        # print('xxx--',data_out, type(data_out))
        # 1/0
        return Response(serializer.data, status=200)
    
    def post(self, request):
        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            detail.update({
                'school': School.objects.get(user=request.user).pk
            })
            # print('----------------------------' check type)
            name = detail['name']
            objs = Grade.objects.filter(name=name)
            if objs.exists():
                return Response('duplicated grade', status=400)


            serializer = GradeSerializer(data=detail, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response('create success', status=200)
            else:
                print('--------------------------qqqq')
                return Response(serializer.errors, status=400)

        if act == 'update':
            grades = Grade.objects.filter(name=data['old name'], school__user=request.user)
            # print('--------------------------------ssss',Grade.objects.filter(pk=data['pk'], school__user=request.user))
            name = detail['name']
            # print('-------------------------------ddddd', detail['name'])
            objs = Grade.objects.filter(name=name)
            if objs.exists():
                return Response('duplicated update', status=400)
            
            if not grades.exists():
                return Response('unable to update', status=400)
            
            grades.update(**data['detail'])
            return Response('update success', status=200)
            # print('---',data)
            # print('----data[pk]', data['pk'])
            # grades = Grade.objects.filter(pk=data['pk'])
            # print('-----students', grades, type(grades))
            # grades.update(**data['detail'])
            # return ...
        
        if act == 'delete':
            grades = Grade.objects.filter(
                name=data['detail']['name'], 
                description=data['detail']['description'], 
                school__user=request.user)
            delete_schools = grades.delete()
            if not grades.exists():
                return Response('delete success', status=200)
            else:
                return Response('unable to delete', status=400)
        
        return Response('failed, action is required', status=400)
            

class APIStudent(APIView):
    def get (self, request):
        data = request.GET.dict()
        objs = Student.objects.filter(grade__school__user=request.user)
        obj = objs.first()
        serializer = StudentSerializer(obj, many=False)
        return Response(serializer.data, status=200)
    
    def post (self, request):
        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        # print('-----------------result', data)
        if act == 'create':
            detail.update({
                'grade': Grade.objects.get(school__user=request.user).pk
            })
            first_name = detail['first_name']
            last_name = detail['last_name']
            nick_name = detail['nick_name']
            objs = Student.objects.filter(first_name=first_name, last_name=last_name, nick_name=nick_name)
            if  objs.exists():
                return Response('duplicated student', status=400)

            serialzer = StudentSerializer(data=detail, many=False)
            if serialzer.is_valid():
                serialzer.save()
                return Response('create success', status=200)
            else:
                return Response(serialzer.errors, status=400)
    
        if act == 'update':
            students = Student.objects.filter(
                first_name=data['old_first_name'],
                last_name=data['old_last_name'],
                nick_name=data['old_nick_name'], 
                grade__school__user=request.user)
            #check duplicate
            first_name = detail['first_name']
            last_name = detail['last_name']
            nick_name = detail['nick_name']
            objs = Student.objects.filter(first_name=first_name, last_name=last_name, nick_name=nick_name)
            if  objs.exists():
                return Response('duplicated student', status=400)


            if not students.exists():
                return Response('unable to update', status=400)
    
            students.update(**request.data['detail'])
            return Response('update success', status=200)
        
        if act == 'delete':
            students = Student.objects.filter(
                first_name=data['detail']['first_name'], 
                last_name=data['detail']['last_name'], 
                nick_name=data['detail']['nick_name'],
                grade__school__user=request.user)
            delete_student = students.delete()
            if not students.exists():
                return Response('delete success', status=200)
            # delete_schools = School.objects.filter(user=request.user).delete()
            else:
                return Response('unable to delete', status=400)
        
        return Response('failed, action is required', status=400)


class APIParent(APIView):
    def get (self, request):
        data = request.GET.dict()
        this_user = request.user
        objs = Parent.objects.filter(director=this_user)
        obj = objs.first()
        serializer = ParentOutSerializer(obj, many=False)
        return Response(serializer.data,status=200)

    def post(self, request):
        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            detail.update({
                'director':request.user.pk
            })
            first_name = detail['first_name']
            last_name = detail['last_name']
            objs = Parent.objects.filter(first_name=first_name, last_name=last_name)
            if objs.exists():
                return Response('duplicated parent', status=400)
            
            #make another action --> create children
            # # children_f = Student.objects.filter(first_name=detail['first_name'], last_name=detail['last_name'], nick_name=detail['nick_name'])
            # childrens = Student(first_name=detail['first_name'], last_name=detail['last_name'], nick_name=detail['nick_name'])
            # childrens.save()
            
            # p1 = Parent (first_name=first_name, last_name=last_name)
            # p1.save()

            # p1.children.add(childrens)

            serializer = ParentInSerializer(data=detail, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response('create success', status=200)
            else:
                return Response(serializer.errors, status=400)
        
        if act == 'add children':
            this_user = request.user
            data = request.data
            parents = Parent.objects.filter(director=this_user)
            # parent = parents.first().id
            print('---------------------------22', parents)

            students = Student.objects.filter(
                first_name=data['detail']['first_name'],
                last_name=data['detail']['last_name'],
                nick_name=data['detail']['nick_name'],)
            print('-------------------------11', students)

            adding = parents.children.add(students)
            
            return Response('children added', status=200)
            
            
        
        if act == 'update':
            this_user = request.user
            parents = Parent.objects.filter(director=this_user)
            first_name = detail['first_name']
            last_name = detail['last_name']
            objs = Parent.objects.filter(first_name=first_name, last_name=last_name)
            if objs.exists():
                return Response('duplicated parent', status=400)

        
            if not parents.exists():
                return Response('unable to update', status=400)
            
            parents.update(**request.data['detail'])
            return Response('update success', status=200)
        
        if act == 'delete':
            this_user = request.user
            parents = Parent.objects.filter(
                first_name=data['detail']['first_name'], 
                last_name=data['detail']['last_name'], 
                director=this_user)
            delete_schools = parents.delete()
            if not parents.exists():
                return Response('delete success', status=200)
            else:
                return Response('unable to delete', status=400)
        
        return Response('failed, action is required', status=400)
