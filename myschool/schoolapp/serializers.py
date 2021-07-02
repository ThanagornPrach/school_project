from django.db.models import fields
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        # fields = ['name', 'description']
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        # fields = ['name', 'description']
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
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

