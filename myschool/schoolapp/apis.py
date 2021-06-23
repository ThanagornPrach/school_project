from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

class APISchool(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        data = request.GET.dict()
        objs = School.objects.filter(**data)
        print('====================result', objs)
        serializer = SchoolSerializer(objs, many=True)
        # print('-----------------------resutl', serializer)
        return Response('success', status=200)

    def post(self, request):
        # user = User.objects.get(username='prach')
        # token_of_prach = Token.objects.get(user = user)
        # token_ = 'Token fd4dad10a051f7c4668245155c7324b28e172c15'
        # print('token of prach=', token_of_prach.key == token_)
        # print(request.user, '------aaa')
        # 12/0

        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            serializer = SchoolSerializer(data=detail, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response('success', status=200)
            else:
                return Response(serializer.errors, status=400)

        if act == 'update':
            # get school of this user
            this_user = request.user
            schools = School.objects.filter(user=this_user)
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

            return Response('s', status=200)

class APIGrade(APIView):
    def get(self, request):
        data = request.GET.dict()
        objs = Grade.objects.filter(**data)
        print('------------------------result', objs)
        serializer = GradeSerializer(objs, many=True)
        return Response('success', status=200)
    
    def post(self, request):
        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            serializer = GradeSerializer(data=detail, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response('create success', status=200)
            else:
                return Response(serializer.errors, status=400)
        
        if act =='update':
            grades = Grade.objects.filter(grade=data['grade'])
            if not grades.exist():
                return ...
        
            grades.update(**detail)
            return Response('success', status=201)
