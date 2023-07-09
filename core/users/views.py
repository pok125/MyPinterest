from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import MultipleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from articles.models import Article
from users.decorators import ownership_required

has_ownership = [login_required, ownership_required]


class SignUp(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('users:test')
    template_name = 'users/sign_up.html'


class SignIn(LoginView):
    template_name = 'users/sign_in.html'


class SignOut(LogoutView):
    pass


class MyPage(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = 'target_user'
    template_name = 'users/mypage.html'

    def get_context_data(self, **kwargs: Any):
        article_list = Article.objects.filter(writer=self.get_object())
        return super().get_context_data(object_list=article_list, **kwargs)


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class UserDelete(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:signin')