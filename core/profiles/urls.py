from django.urls import path
from profiles.views import *
app_name = 'profiles'

urlpatterns = [
    path('create/', ProfileCreate.as_view(), name='create'),
]