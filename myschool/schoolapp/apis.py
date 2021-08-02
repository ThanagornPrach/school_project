from os import name, path
from unittest.case import skip
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
            #make sure that the format 'username'/'password' is correct
            try:
                username = detail['username']
                password = detail['password']
            except:
                return Response('incorrect format', status=400)

            objs = User.objects.filter(username=username)
            if objs.exists():
                return Response('duplicated username', status=400)

            new_user = User.objects.create_user(username=username, password=password)
            # print('-------------------ss',)
            # 1/0
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

            try:
                username = detail['username']
                password = detail['password']
                # old_name = data['old username']
            except:
                return Response('incorrect format', status=400)
            
            objs = User.objects.filter(username=username, user=this_user)
            if objs.exists():
                return Response('duplicated update', status=400)
            
            if not users.exists():
                return Response('unable to update', status=400)
            
            users.update(**request.data['detail'])
            return Response('update success', status=200)
        
        if act == 'delete':
            this_user = request.user

            try:
                username = detail['username']
                password = detail['password']
            except:
                return Response('incorrect format', status=400)

            users = User.objects.filter(username=this_user)
            if not users.exists():
                return Response('no user', status=400)

            users.delete()
            return Response('delete success', status=200)
        
    #check whether user insert correct input for 'act'
        else:
            return Response('act is incorrect', status=400)


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
            
            try:
                name = detail['name']
                description = detail['description']
            except:
                return Response('incorrect format', status=400)
            
            objs = School.objects.filter(name=name,description=description, user=request.user)
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
            try:
                # check duplicated name
                if 'name' in detail:
                    name = detail['name']
                    objs = School.objects.filter(user=request.user, name=name)
                    if objs.exists():
                        return Response('duplicated name! you cannot use this name', status=400)

                objs = School.objects.filter(user=request.user)
                objs.update(**detail)   
                return Response('update success', status=200)
            except:
                return Response('incorrect format', status=400)

        # if act == 'update_xxx':
        #     # get school of this user
        #     this_user = request.user
        #     try:
        #         school_pk = detail['school_pk']
        #     except:
        #         return Response('incorrect format', status=400)
        #     schools = School.objects.filter(pk=school_pk, user=this_user)
        #     # print('--------------------------ans',School.objects.filter(user=this_user))

        #     print('---------------------------', detail)
            

        #     try:
        #         name = detail['name']
        #         description = detail['description']
        #         # if 'description' not in detail.keys():
        #         #     objs = School.objects.filter(name=name)
        #         #     if objs.exists():
        #         #         return Response('duplicated school', 400)


        #         #     if not schools.exists():
        #         #         return Response('fail', status=400)
                    
        #         #     del detail['school_pk']

        #         #     schools.update(**detail)
        #         #     return Response('update success', status=200)
                
        #         # if description not in detail.keys():
        #         #     del description
        #     except:
        #         return Response('incorrect format', status=400)

        #     objs = School.objects.filter(name=name, user=this_user)
        #     if objs.exists():
        #         return Response('duplicated school', 400)


        #     if not schools.exists():
        #         return Response('fail', status=400)

        #     # # approach 1 - single update
        #     # # get new school name from user
        #     # new_code = request.data['detail']['school']
        #     # obj = schools[0]
        #     # obj.school = new_code
        #     # obj.save()
        #     del detail['school_pk']
        #     # # approach 2 - multi update #update all schools(object) that the user requested
        #     schools.update(**detail)

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
        
        if act == 'delete':
            this_user = request.user
            try:
                school_pk = detail['school_pk']
            except:
                return Response('incorrect format', status=400)

            schools = School.objects.filter(pk=school_pk, user=this_user)
            print('----------------------------11', schools)
            if not schools.exists():
                return Response('unable to delete', status=400)

            schools.delete()
            print('----------------de', schools)
            return Response('delete success', status=200)
        
        else:
            return Response('act is incorrect', status=400)
            
        
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
        if act == 'create':
            # print('----------------------dfd', detail['names'])
            # 12/0

            #get school
            schools = School.objects.filter(user=request.user)
            if len(schools) != 1:
                return Response('this user has no school', status=400)
            school = schools.first()
            
            # python function as variable
            if type(detail) != list:
                return Response('not correct detail format', status=400)

            for dat_dict in detail:
                # check key is correct?
                for key in dat_dict.keys():
                    if key not in ['name', 'description']:
                        return Response('incorrect format; you only create grade with "name" and "description";', status=400)

                # check duplicated
                new_name = dat_dict['name']
                grades = Grade.objects.filter(school__user=request.user, name=new_name)
                if grades.exists():
                    return Response('dup', status=400)

                # add school pk to dictionary
                dat_dict['school'] = school.pk

                # dicti = {
                #     'name' : ....,
                #     'description': ....,
                #     'school': .....,
                # }
            
            serializer = GradeSerializer(data=detail, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response('create %d success'%len(detail), status=200)
            else:
                return Response(serializer.errors, status=400)


        if act == 'update':

            try:
                for dict in detail:
                    key_pk = dict['pk']
                    key_name = dict['name']
                    key_description = dict['description']
            except:
                return Response('incorrect format', status=400)
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
            pk = detail['pk']
            grades = Grade.objects.filter(
                pk=pk, 
                school__user=request.user)
            if not grades.exists():
                return Response('unable to delete', status=400)
            
            grades.delete()
            return Response('delete success', status=200)
        
        else:
            return Response('act is incorrect', status=400)
            

            
        
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
            try:
                grade_pk = detail['grade']
            except:
                return Response('incorrect format', status=400)
            # print('---------------------------gg', grade)

            #add student to grade
            grades = Grade.objects.filter(pk=grade_pk, school__user=request.user)
            if not grades.exists():
                return Response('no pk', status=400)
            
            #check duplicated name and key
            try:
                first_name = detail['first_name']
                last_name = detail['last_name']
                nick_name = detail['nick_name']
            except:
                return Response('incorrect format', status=400)
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
            try:
                student_pk = detail['student_pk']
            except:
                return Response('incorrect format', status=400)
            print('-----------------------asd', student_pk)
            students = Student.objects.filter(
                pk=student_pk,
                grade__school__user=request.user)
            print('-------------------------pk', students)
            if not students.exists():
                return Response('no pk', status=400)
            
            #check duplicate and key
            try:
                first_name = detail['first_name']
                last_name = detail['last_name']
                nick_name = detail['nick_name']
            except:
                return Response('incorrect format', status=400)
            objs = Student.objects.filter(
                first_name=first_name, 
                last_name=last_name, 
                nick_name=nick_name, grade__school__user=request.user)
            print('----------------------kgkgk')
            if  objs.exists():
                return Response('duplicated student', status=400)

            del detail['student_pk']
            
            # update student
            students.update(**detail)
            return Response('update success', status=200)
        
        if act == 'delete':
            student_pk = detail['student_pk']
            print('---------------------------ff', student_pk)
            students = Student.objects.filter(
                pk=student_pk,
                grade__school__user=request.user)
            print('-0------------------------------dfff', students)
            if not students.exists():
                return Response('no student to delete', status=400)
            print('--------------------------sss', students)
            # delete_schools = School.objects.filter(user=request.user).delete()
            students.delete()
            print('---------------cc', students)
            return Response('delete success', status=200)
        
        else:
            return Response('act is incorrect', status=400)
        
        # return Response('failed, action is required', status=400)


class APIParent(APIView):
    def get (self, request):
        # data = request.GET.dict()
        this_user = request.user
        objs = Parent.objects.filter(director=this_user)
        obj = objs.first()
        serializer = ParentOutSerializer(obj, many=False)
        return Response(serializer.data,status=200)

    def post(self, request):
        data = request.data
        for k in ['act', 'detail']:
            if k not in data.keys():
                return Response('failed, %s is required'%k, status=400)
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            detail.update({
                'director':request.user.pk
            })
            
            try:
                first_name = detail['first_name']
                last_name = detail['last_name']
            except:
                return Response('incorrect fomat', status=400)
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
                "detail": {
                    "parent_pk": "pk",
                    "children_pk": [{"pk":"1"}, {"pk":"17"}, {"pk": "10"}]
                }
            }
            '''

            try:
                parent_pk = data['detail']['parent_pk']
                children_pk = data['detail']['children_pk']
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
            try:
                parent_pk = detail['parent_pk']
            except:
                return Response('incorrect format', status=400)
            print('------------------------111', parent_pk)
            this_user = request.user
            parents = Parent.objects.filter(pk=parent_pk, director=this_user)
            print('--------------------------dddd', parents)

            #check duplicated update and key
            try:
                first_name = detail['first_name']
                last_name = detail['last_name']
            except:
                return Response('incorrect format', status=400)
            objs = Parent.objects.filter(first_name=first_name, last_name=last_name, director=this_user)
            if objs.exists():
                return Response('duplicated parent', status=400)

        
            if not parents.exists():
                return Response('unable to update', status=400)
            
            del detail['parent_pk']
            parents.update(**detail)
            return Response('update success', status=200)
        
        if act == 'delete':
            this_user = request.user
            print('---------------------33', this_user)
            parent_pk = detail['parent_pk']
            parents = Parent.objects.filter(
                pk=parent_pk,
                director=this_user)
            
            print('--------------------------------22', parents)
            if not parents.exists():
                return Response('no parent', status=400)
            
            parents.delete()
            # print('--------------------de',parents)
            return Response('delete success', status=200)
            
        return Response('failed, action is required', status=400)
