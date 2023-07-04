from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    path('test', test, name='test'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('signout/', SignOut.as_view(), name='signout'),
]