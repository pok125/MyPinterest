from django.urls import path
from profiles.views import *

app_name = 'profiles'

urlpatterns = [
    path('mypage/<int:user_id>/', ProfileView.as_view(), name='mypage'),
    path('update/<int:profile_id>/', ProfileUpdateView.as_view(), name='update'),
]