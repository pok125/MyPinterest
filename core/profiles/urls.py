from django.urls import path
from profiles.views import *

app_name = 'profiles'

urlpatterns = [
    path('mypage/<int:user_id>', ProfileView.as_view(), name='mypage'),
    # path('create/', ProfileCreate.as_view(), name='create'),
    # path('update/<int:pk>', ProfileUpdate.as_view(), name='update'),
]