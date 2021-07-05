from .apis import *
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('school/', APISchool.as_view()),
    path('grade/', APIGrade.as_view()),
    path('student/', APIStudent.as_view()),
    path('parent/', APIParent.as_view()),
    path('user/', APIUser.as_view()),
    path('get-all-student-name/', APIAllStudent.as_view())
]