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
from django.contrib.auth import login, authenticate
from .forms import JoinForm, LoginForm

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


class JoinView(View):
    # 회원가입 페이지
    def get(self, request):
        user = request.user

        # 이미 로그인 한 상태인 유저
        # if user.is_authenticated:
        #     return redirect('')
        
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
            print(form.data)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            print(email, password)
            # user 유효성 검사
            user = authenticate(username=email, password=password)
            print(user)
            if user:
                return redirect('users:login')
        
        messages.add_message(self.request, messages.ERROR, '회원가입에 실패했습니다.')
        context = {
            'form': form
        }
        return render(request, 'users/join.html', context=context)