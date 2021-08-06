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
        
        if act == 'update':
            this_user = request.user
            users = User.objects.filter(username=this_user)
            
            if type(detail) != dict:
                return Response('incorrect format', status=400)

            for key in detail:
                if key not in ['username','password']:
                    return Response('incorrect format', status=400)
            
            username = detail['username']
            
            objs = User.objects.filter(username=username)
            print('-----------------obf', objs)
            if objs.exists():
                return Response('duplicated username', status=400)
            
            if not users.exists():
                return Response('unable to update', status=400)
            
            users.update(**detail)
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
        
        #latest change: 3/8
        if act == 'create':
            #check detail format
            if type(detail) != dict:
                return Response('incorrect detail format', status=400)

            #bring user.pk
            detail.update({
                'user':request.user.pk
            })
            
            #check user
            user = User.objects.filter(username=request.user)
            if len(user) != 1:
                return Response('no user', status=400)
            
            #check name and its duplication
            if 'name' in detail:
                name = detail['name']
                objs = School.objects.filter(name=name, user=request.user)
                if objs.exists():
                    return Response ('duplicated school', status=400)
            else:
                return Response('incorrect format', status=400)

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
                print('---------------------d',detail)
                if 'name' in detail:
                    print('--------------------')
                    name = detail['name']
                    objs = School.objects.filter(user=request.user, name=name)
                    if objs.exists():
                        return Response('duplicated name! you cannot use this name', status=400)

                schools = School.objects.filter(user=request.user)
                if not schools.exists():
                    return Response('no school')
                print('-----------------sss', detail)
                schools.update(**detail) 
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

        #latest change: 2/8
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
                        return Response('incorrect format; you only create grade with "name" or "description";', status=400)

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

            if type(detail) != list:
                return Response('incorrect detail format', status=400)

            for dict in detail:
                for key in dict.keys():
                    if key not in ['name', 'description', 'pk']:
                        return Response('incorrect format', status=400)
            
            print('-----------------detail',detail)

            new_names = []
            for dat in detail:
                print('--------------------dat', dat)
                if 'name' in dat:
                    name = dat['name']
                    new_names.append(name)
                    print('-------------------------ert', new_names)
            db_objs = Grade.objects.filter(name__in=new_names, school__user=request.user)
            #use this technique to work with list
            print('----------------------------sdsdsd', db_objs)
            if db_objs.exists():
                return Response('duplicated name', status=400)
            

            for dat in detail:
                print('-----------------------dat ', dat)
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

            return Response('update %d success'%len(detail), status=200)
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
        # obj = objs.first()
        serializer = StudentSerializer(objs, many=True)
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
            objs = Student.objects.filter(
                first_name=first_name, 
                last_name=last_name, 
                nick_name=nick_name, 
                grade__school__user=request.user)
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
            #check detail format
            if type(detail) != dict:
                return Response('incorrect detail format', status=400)

            #check whether the user spell them correctly, not to check if the user have them in the postman or not 
            for key in detail:
                if key not in ['student_pk','first_name','last_name','nick_name']:
                    return Response('incorrect format', status=400)

            '''''
                {
                    "act": "update",
                    "detail": {
                        "student_pk": "1",
                        "first_name": "bom",
                        "last_name": "bomus",
                        "nick_name": "bom-bom"
                    }
                }
            '''''
            
            if 'first_name' in detail and 'last_name' in detail:
                first_name = detail['first_name']
                last_name = detail['last_name']
                
                students = Student.objects.filter(
                    first_name=first_name, 
                    last_name=last_name,
                    grade__school__user=request.user)
                if students.exists():
                    return Response('unable to apply first name and last name due to the names already existed', status=400)
            
            #pk must be in [detail]
            if 'student_pk' in detail:
                pk = detail['student_pk']
            else:
                return Response('student_pk has to be in [detail]', status=400)
            #check pk
            students = Student.objects.filter(pk=pk, grade__school__user=request.user)
            if not students.exists():
                return Response('no student_pk', status=400)
            
            # updating
            del detail['student_pk']

            students.update(**detail)
            return Response('update success', status=200)

            # try:
            #     student_pk = detail['student_pk']
            # except:
            #     return Response('incorrect format', status=400)
            # print('-----------------------asd', student_pk)
            # students = Student.objects.filter(
            #     pk=student_pk,
            #     grade__school__user=request.user)
            # print('-------------------------pk', students)
            # if not students.exists():
            #     return Response('no pk', status=400)
            
            # #check duplicate and key
            # try:
            #     first_name = detail['first_name']
            #     last_name = detail['last_name']
            #     nick_name = detail['nick_name']
            # except:
            #     return Response('incorrect format', status=400)
            # objs = Student.objects.filter(
            #     first_name=first_name, 
            #     last_name=last_name, 
            #     nick_name=nick_name, grade__school__user=request.user)
            # print('----------------------kgkgk')
            # if  objs.exists():
            #     return Response('duplicated student', status=400)

            # del detail['student_pk']
            
            # # update student
            # students.update(**detail)
            # return Response('update success', status=200)
        
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
            if type(detail) != dict:
                return Response('incorrect detail format', status=400)

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
            if type(detail) != dict:
                return Response('incorrect detail format', status=400)

            try:
                parent_pk = detail['parent_pk']
                children_pk = detail['children_pk']
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
            if type(children_pk) != list:
                return Response('incorrect children_pk format', status=400)

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
            '''''
            {
                "act": "update",
                "detail": {
                    "parent_pk": "1",
                    "first_name": "tom (this is new name [first_name])",
                    "last_name": "tom-tom (this is new [last_name])"
                }
            }
            '''''
            if type(detail) != dict:
                return Response('incorrect detail format', status=400)

            for key in detail:
                if key not in ['first_name','last_name','parent_pk']:
                    return Response('incorrect format', status=400)
            
            if 'first_name' in detail:
                first_name = detail['first_name']
                f_name = Parent.objects.filter(first_name=first_name, director=request.user)
                if f_name.exists():
                    return Response('duplicated first name', status=400)
            
            if 'last_name' in detail:
                last_name = detail['last_name']
                l_name = Parent.objects.filter(last_name=last_name, director=request.user)
                if l_name.exists():
                    return Response('duplicated last name', status=400)
            
            # for name in detail:
            #     if name in ['first_name', 'last_name']:
            #         first_name = detail['first_name']
            #         last_name = detail['last_name']
            # names = Parent.objects.filter(
            #     first_name=first_name,
            #     last_name=last_name,
            #     director=request.user)
            # if names.exists():
            #     return Response('duplicated %s'%name, status=400)

            if 'parent_pk' not in detail:
                return Response('parent_pk must be in [detail]', status=400)
            
            pk = detail['parent_pk']
            parents = Parent.objects.filter(pk=pk, director=request.user)
            if not parents.exists():
                return Response('no parent_pk', status=400)
            
            del detail['parent_pk']

            parents.update(**detail)
            return Response('update success', status=200)
            # try:
            #     parent_pk = detail['parent_pk']
            # except:
            #     return Response('incorrect format', status=400)
            # print('------------------------111', parent_pk)
            # this_user = request.user
            # parents = Parent.objects.filter(pk=parent_pk, director=this_user)
            # print('--------------------------dddd', parents)

            # #check duplicated update and key
            # try:
            #     first_name = detail['first_name']
            #     last_name = detail['last_name']
            # except:
            #     return Response('incorrect format', status=400)
            # objs = Parent.objects.filter(first_name=first_name, last_name=last_name, director=this_user)
            # if objs.exists():
            #     return Response('duplicated parent', status=400)

        
            # if not parents.exists():
            #     return Response('unable to update', status=400)
            
            # del detail['parent_pk']
            # parents.update(**detail)
            # return Response('update success', status=200)
        
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
