from django.db.models import fields
from django.db.models.query import prefetch_related_objects
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        # exclude = ['id']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        # fields = ['name', 'description']
        fields = '__all__'
        # exclude = ['id']


class GradeSerializer(serializers.ModelSerializer):
    # school_name = serializers.CharField(max_length=255)
    # name = serializers.JSONField()
    class Meta:
        model = Grade
        # fields = ['name', 'description']
        fields = '__all__'


    # @property
    # def data(self):
    #     ret = super(Serializer, self).data
    #     print('----ret', ret, type(ret))
    #     return ReturnDict(ret, serializer=self)

    # def __init__(self, *args, **kwargs):
    #     self.serializer = kwargs.pop('serializer')
    #     super(ReturnDict, self).__init__(*args, **kwargs)

        
class StudentSerializer(serializers.ModelSerializer):
    # def parent(self, obj):
    #     # lst = [obj]
    #     # parents = Parent.objects.filter(children__in=lst)
    #     # parent = parents.first()
    #     # return 
    #     return 'hi'
    parent = serializers.ReadOnlyField()
    class Meta:
        model = Student
        # fields = ['first_name', 'last_name', 'nick_name']
        fields = '__all__'

class ParentInSerializer(serializers.ModelSerializer):  #In = into the database 
    class Meta:
        model = Parent
        # fields = ['first_name', 'last_name']
        # fields = '__all__'
        exclude = ['children']

class ParentOutSerializer(serializers.ModelSerializer): #Out = show to the user 
    class Meta:
        model = Parent
        fields = '__all__'

# class StudentOnlyNameSerializer( serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['grade', ]
# class SchoolOnlyDescriptionSerializer( serializers.ModelSerializer):
#     class Meta:
#         model = School
#         fields = ['description', ]

