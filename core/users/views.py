from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import FollowRecord
from .forms import JoinForm, LoginForm
from profiles.models import Profile

User = get_user_model()

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
            user = form.save()
            Profile.objects.create(user=user)

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


### UserDelete
class UserDeleteView(LoginRequiredMixin, View):
    # 회원탈퇴 요청
    def post(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(User, pk=user_id)

        if user != target_user:
            return HttpResponseBadRequest()
        
        target_user.delete()

        return redirect('home')


### Following
class FollowingView(LoginRequiredMixin, View):
    # 팔로우 요청
    def get(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(User, pk=user_id)
        FollowRecord.objects.create(following_user=user, followed_user=target_user) 
        
        return redirect('profiles:mypage', user_id=target_user.pk)


class UnFollowingView(LoginRequiredMixin, View):
    # 팔로우 취소
    def get(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(User, pk=user_id)
        follow_record = FollowRecord.objects.filter(following_user=user, followed_user=target_user)

        if follow_record.exists():
            follow_record.delete()

        return redirect('profiles:mypage', user_id=target_user.pk)