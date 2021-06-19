from .apis import *
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('test1/', TestSchool.as_view()),
    # path('test2/', TestSeasons.as_view()),
]