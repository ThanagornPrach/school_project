from .apis import *
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('test1/', APISchool.as_view()),
    path('test2/', APIGrade.as_view()),
]