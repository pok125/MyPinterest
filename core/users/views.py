# from typing import Any, Dict
# from django.urls import reverse_lazy, reverse
# from django.views.generic import CreateView, DetailView, DeleteView
# from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.views.generic.list import MultipleObjectMixin
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# from articles.models import Article
# from users.decorators import ownership_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .forms import JoinForm, LoginForm

User = get_user_model()
# has_ownership = [login_required, ownership_required]


# class SignUp(CreateView):
#     model = User
#     form_class = UserCreationForm
#     success_url = reverse_lazy('users:test')
#     template_name = 'users/sign_up.html'


# class SignIn(LoginView):
#     template_name = 'users/sign_in.html'


# class SignOut(LogoutView):
#     pass


# class MyPage(DetailView, MultipleObjectMixin):
#     model = User
#     context_object_name = 'target_user'
#     template_name = 'users/mypage.html'

#     def get_context_data(self, **kwargs: Any):
#         article_list = Article.objects.filter(writer=self.get_object())
#         return super().get_context_data(object_list=article_list, **kwargs)


# @method_decorator(has_ownership, 'get')
# @method_decorator(has_ownership, 'post')
# class UserDelete(DeleteView):
#     model = User
#     template_name = 'users/delete.html'
#     success_url = reverse_lazy('users:signin')

### Join
class JoinView(View):
    # 회원가입 페이지
    def get(self, request):
        user = request.user

        # 이미 로그인 한 상태인 유저
        if user.is_authenticated:
            messages.add_message(request, messages.ERROR, '로그아웃 후 진행해 주세요.')
            
            return redirect('/')
        
        form = JoinForm()
        context = {
            'form': form
        }
        
        return render(request, 'users/join.html', context=context)
    
    # 회원가입 요청
    def post(self, request): 
        form = JoinForm(request.POST)
        
        # form 유효성 검사
        if form.is_valid():
            form.save()

            return redirect('users:login')
        
        messages.add_message(request, messages.ERROR, '회원가입에 실패했습니다.')
        
        context = {
            'form': form
        }

        return render(request, 'users/join.html', context=context)


### Login
class LoginView(View):
    # 로그인 페이지
    def get(self, request):
        user = request.user

        # 이미 로그인된 유저
        if user.is_authenticated:
            messages.add_message(request, messages.ERROR, '이미 로그인된 상태입니다.')
            
            return redirect('/')
        
        form = LoginForm()
        context = {
            'form': form
        }

        return render(request, 'users/login.html', context=context)
    
    # 로그인 요청
    def post(self, request):
        form = LoginForm(request, request.POST)
        
        # form 유효성 검사
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            # 해당 입력 정보에 대한 유저검사
            if user:
                login(request, user)
        
                return redirect('/')

        messages.add_message(request, messages.ERROR, '입력하신 정보가 유효하지 않습니다.')

        context = {
            'form': form
        }

        return render(request, 'users/login.html', context=context)


### Logout
class LogoutView(View):
    # 로그아웃 요청
    def get(self, request):
        logout(request)
        
        return redirect('/')