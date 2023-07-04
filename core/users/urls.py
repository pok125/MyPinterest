from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    path('test', test, name='test'),
    path('signup', SignUp.as_view(), name='signup'),
]