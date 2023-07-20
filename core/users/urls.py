from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    path('join/', JoinView.as_view(), name='join'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:user_id>', UserDeleteView.as_view(), name='delete'),
]