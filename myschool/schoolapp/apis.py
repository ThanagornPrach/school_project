from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *

class TestSchool(APIView):
    def get(self,request):
        data = request.GET.dict()
        objs = School.objects.filter(**data)
        serializer = SchoolSerializer(objs, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data
        act = data.get('act')
        detail = data.get('detail')
        if act == 'create':
            serializer = SchoolSerializer(data=detail, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response('success', status=201)
            else:
                return Response(serializer.errors, status=400)
        
        if act == 'update':
            obj = School.objects.filter('school')
            serializer = obj.update(**detail)
            return Response('update', status=201)
        else:
            return Response('Unable to update', status=400)
