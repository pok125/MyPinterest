from django.urls import path
from .views import *

app_name = 'comment'

urlpatterns = [
    path('create/', CommentCreate.as_view(), name='create'),
]
