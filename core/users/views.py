from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from users.decorators import ownership_required
from django.contrib.auth.decorators import login_required

has_ownership = [login_required, ownership_required]

def test(request):
    return render(request, 'base.html')


class SignUp(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('users:test')
    template_name = 'users/sign_up.html'


class SignIn(LoginView):
    template_name = 'users/sign_in.html'


class SignOut(LogoutView):
    pass


class MyPage(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'users/mypage.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class UserDelete(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:signin')