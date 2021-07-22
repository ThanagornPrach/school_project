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
        # data = request.GET.dict()
        this_user = request.user
        objs = User.objects.filter(username=this_user)
        obj = objs.first()
        serializer = UserSerializer(obj, many=False)
        return Response(serializer.data, status=200)
    
    def post(self, request): 
        data = request.data
        for k in ['act','detail']:
            if k not in data.keys():
                return Response('failed, %s is required'%k, status=400)
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
            
            users.update(**request.data['detail'])
            return Response('update success', status=200)
        
        if act == 'delete':
            this_user = request.user
            users = User.objects.filter(username=this_user)
            users.delete()
            return Response('delete success', status=200)
        else:
            return Response('unable to delete', status=400)



class APISchool(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        # data = request.GET.dict()
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
        for k in ['act','detail']:
            if k not in data.keys():
                return Response('failed, %s is required'%k, status=400)
        if act == 'create':
            detail.update({
                'user':request.user.pk
            })
            name = detail['name']
            objs = School.objects.filter(name=name, user=request.user)
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
            print('----------------------------11', schools)
            schools.delete()
            if not schools.exists():
                return Response('delete success', status=200)
            else:
                return Response('unable to delete', status=400)
        
        # we can check 'act' like the way belowm, but it is not quite effective as the one above
        # return Response('failed, action is required', status=400)     

# class APIAllStudent(APIView):
#     model = Student
#     serializer = StudentOnlyNameSerializer
#     def get(self, request):
#         objs = self.model.objects.all()
#         ser = self.serializer(objs, many=True)
#         print('---------------------------hhh', type(objs))
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
        # data = request.GET.dict()
        objs = Grade.objects.filter(school__user=request.user)
        # obj = objs.first()

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
        serializer = GradeSerializer(objs, many=True)
        # data_out = serializer.data
        # print('xxx--',data_out, type(data_out))
        # 1/0
        return Response(serializer.data, status=200)
    
    def post(self, request):
        data = request.data
        for k in ['act', 'detail']:
            if k not in data.keys():
                return Response('failed, %s is required'%k, status=400)
        act = data.get('act')
        # print('-----------------ko',act)
        # 15/0
        detail = data.get('detail')
        # print('---------------------------eee',detail)
        if act == 'create':
            """
            # create grade
            POST /api/v1/grade/
            ```json
                "act": "create",
                "detail": {
                    "namessssss": [{"name":"1"}, {"name":"17"}, {"name": "10"}],
                    "description": "this is description"
                }
            }
            ```
            """
            # print('----------------------dfd', detail['names'])
            # 12/0
            schools = School.objects.filter(user=request.user)
            # we can use schools.first or the method below

            # user has no school
            if len(schools) == 1:
                school = schools[0]
            else:
                return Response('user has no school', status=400)

            names = detail['names']
            print('---------------------------ss', names)
            # 11/0
            # query_names = Grade.objects.filter(name=names)
            # if query_names.exists():
            #     return Response('duplicated name', status=400)
            
            for name in names:
                print('---------------------------i', name)
                query_names = Grade.objects.filter(name=name, school__user=request.user)
                print('----------------------er', names)
                print('-------------------------o', query_names)
                if query_names.exists():
                    return Response('duplicated name', status=400)

            description = detail['description']
            print('--------------------------123', description)
            objs = []
            count = 0
            # [(k, v), (k, v), (k, v)]
            for name in detail['names']:
                print('\n\n----------------------------',count)
                print(count, '----name', name)

                obj = {
                    'school': school.pk,

                    'name': name,
                    'description': description,
                }
                # obj.update({
                #     'school': school
                # })

                print(count, '---- obj', obj)
                objs.append(obj)
                print(count, '---- objs []', objs)
                count += 1
            # [{'school':pk_of_choull', 'name': 'grade1', 'description': 'des1'}, {'name': 'grade2', 'description': 'des2'}]
            print('xxx--------------objs=',objs)

            serializer = GradeSerializer(data=objs, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response('create %d success'%count, status=200)
            else:
                return Response(serializer.errors, status=400)


        if act == 'update':


            # old_names = data['pk_names']
            # print('-----------------------jj', old_names)
            # new_names = detail['names']
            # for pk_name in old_names:
            #     print('=======================', pk_name)
            #     grades = Grade.objects.filter(pk=pk_name, school__user=request.user)
            #     print('========================gg',grades)
            #     if not grades.exists():
            #         return Response('pk does not exist', status=400)
            #     detail = request.data['detail']
            #     detail['name'] = 
            #     grades.update(**request.data['detail'])
            #     print('----------------------------ii', request.data['detail'])
            #     1/0
            #     print(grades)
            
            # check duplicate update
            # new_name = detail
            # print('============================sss', new_name)
            
            new_names = []
            for dat in detail:
                name = dat['name']
                new_names.append(name)
                print('-------------------------ert', new_names)
            db_objs = Grade.objects.filter(name__in=new_names, school__user=request.user)
            #use this technique to work with list
            print('----------------------------sdsdsd', db_objs)
            if db_objs.exists():
                return Response('duplicated name', status=400)
            

            for dat in detail:
                pk = dat['pk']
                print('============================as', pk)
                grades = Grade.objects.filter(school__user=request.user, pk=pk)
                if not grades.exists():
                    return Response('pk does not exist', status=400)

                if len(grades) == 1:
                    # traditional approach
                    # grades.update({
                    #     "name": dat['name'],
                    #     "descriptions": dat['descriptions']
                    # })

                    # smart approach
                    del dat['pk']

                    # let's update 
                    grades.update(**dat)

            return Response('update success', status=200)
            # grades = Grade.objects.filter(name=data['old names'], school__user=request.user)
            # # print('--------------------------------ssss',Grade.objects.filter(pk=data['pk'], school__user=request.user))
            # name = detail['names']
            # # print('-------------------------------ddddd', detail['name'])
            # objs = Grade.objects.filter(name=name)
            # if objs.exists():
            #     return Response('duplicated update', status=400)
            
            # if not grades.exists():
            #     return Response('unable to update', status=400)
            
            # grades.update(**request.data['detail'])
            # return Response('update success', status=200)
            # # print('---',data)
            # # print('----data[pk]', data['pk'])
            # # grades = Grade.objects.filter(pk=data['pk'])
            # # print('-----students', grades, type(grades))
            # # grades.update(**data['detail'])
            # # return ...
        
        if act == 'delete':
            grades = Grade.objects.filter(
                name=data['detail']['name'], 
                description=data['detail']['description'], 
                school__user=request.user)
            grades.delete()
            if not grades.exists():
                return Response('delete success', status=200)
            else:
                return Response('unable to delete', status=400)
        
        # return Response('failed, action is required', status=400)
            
class APIStudent(APIView):
    def get (self, request):
        # data = request.GET.dict()
        objs = Student.objects.filter(grade__school__user=request.user)
        obj = objs.first()
        serializer = StudentSerializer(obj, many=False)
        return Response(serializer.data, status=200)
    
    def post (self, request):
        data = request.data
        for k in ['act','detail']:
            if k not in data.keys():
                return Response('failed, %s is required'%k, status=400)
        act = data.get('act')
        detail = data.get('detail')
        # print('-----------------result', data)
        if act == 'create':
            grade_pk = detail['grade']
            # print('---------------------------gg', grade)

            #add student to grade
            grades = Grade.objects.filter(pk=grade_pk, school__user=request.user)
            if not grades.exists():
                return Response('no pk', status=400)
            
            #check duplicated name
            first_name = detail['first_name']
            last_name = detail['last_name']
            nick_name = detail['nick_name']
            objs = Student.objects.filter(first_name=first_name, last_name=last_name, nick_name=nick_name, grade__school__user=request.user)
            if  objs.exists():
                return Response('duplicated student', status=400)

            serializer = StudentSerializer(data=detail, many=False)
            # print('---------------------------fgf', serializer)
            if serializer.is_valid():
                serializer.save()
                return Response('create success', status=200)
            else:
                return Response(serializer.errors, status=400)
    
        if act == 'update':
            students = Student.objects.filter(
                first_name=data['old_first_name'],
                last_name=data['old_last_name'],
                nick_name=data['old_nick_name'], 
                grade__school__user=request.user)
            print('----------------------',students)
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
            students.delete()
            if not students.exists():
                return Response('delete success', status=200)
            # delete_schools = School.objects.filter(user=request.user).delete()
            else:
                return Response('unable to delete', status=400)
        
        # return Response('failed, action is required', status=400)


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
        
        # if act == 'add children':
        #     this_user = request.user
        #     # print('--------------------------ss', this_user)
        #     data = request.data
            

        #     parents = Parent.objects.filter(
        #         pk=data['parent'],
        #         director=request.user)

        #     parent = parents.first()
            

        #     students = Student.objects.filter(
        #         pk=data['children'],
        #         grade__school__user=request.user)
            
        #     student = students.first()

          
            
        #     return Response('children added', status=200)

        if act == 'add children':
            data = request.data
            '''  
            this is the data format
            {
                "act": "add children",
                "parent_pk": "pk",
                "children_pk": [{"pk": "1"}, {"pk": "17"}, {"pk": "10"}]
            }
            '''

            try:
                parent_pk = data['parent_pk']
                children_pk = data['children_pk']
                try:
                    parent_pk = int(parent_pk)
                except:
                    return Response('incorrect parent_pk', status=400)
            except:
                return Response('no parent_pk or children_pk', status=400)
            
            # check parent is ready?
            parents = Parent.objects.filter(pk=parent_pk, director=request.user)
            if not parents.exists():
                return Response('incorrect parent pk', status=400)
            parent = parents.first()
            
            # check children is ready
            ready_children = []
            for child in children_pk:
                try:
                    child_pk = child['pk']
                except:
                    return Response('incorrect format', status=400)
                childs = Student.objects.filter(pk=child_pk, grade__school__user=request.user)
                if not childs.exists():
                    return Response('incorrect child pk', status=400)
                
                child = childs.first()
                ready_children.append(child)

            # add children to parent
            count = 0
            for child in ready_children:
                parent.children.add(child)
                count += 1
            
            return Response('added %d child to parent'%count, status=200)
        
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
            print('---------------------33', this_user)
            parents = Parent.objects.filter(
                first_name=data['detail']['first_name'], 
                last_name=data['detail']['last_name'], 
                director=this_user)
            
            print('--------------------------------22', parents)
            if not parents.exists():
                return Response('no parent', status=400)
            
            parents.delete()
            return Response('delete success', status=200)
            
        return Response('failed, action is required', status=400)
