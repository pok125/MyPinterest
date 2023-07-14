from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    # path('signin/', SignIn.as_view(), name='signin'),
    # path('signout/', SignOut.as_view(), name='signout'),
    # path('mypage/<int:pk>', MyPage.as_view(), name='mypage'),
    # path('delete/<int:pk>', UserDelete.as_view(), name='delete'),
    path('join/', JoinView.as_view(), name='join'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]