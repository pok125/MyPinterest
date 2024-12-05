from django.urls import path
from users.views import *

app_name = "users"

urlpatterns = [
    path("join/", JoinView.as_view(), name="join"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete/<int:user_id>", UserDeleteView.as_view(), name="delete"),
    path("following/<int:user_id>", FollowingView.as_view(), name="following"),
    path("unfollowing/<int:user_id>", UnFollowingView.as_view(), name="unfollowing"),
    path("mypage/<int:user_id>/", MyPageView.as_view(), name="mypage"),
    path("update/", MyPageUpdateView.as_view(), name="update"),
]
