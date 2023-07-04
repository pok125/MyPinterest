from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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