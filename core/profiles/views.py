from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm

User = get_user_model()


class ProfileView(View):
    # mypage
    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user_id=user_id)
        context = {
            'target_user': profile.user,
            'profile': profile
        }

        return render(request, 'profiles/mypage.html', context=context)
    

class ProfileUpdateView(LoginRequiredMixin, View):
    # form에 대한 초기 값 세팅을 위해 initial객체 사용
    def get_initial(self, profile):
        initial = dict()
        initial['image'] = profile.image
        initial['message'] = profile.message

        return initial
    
    # 프로필 수정 페이지
    def get(self, request, profile_id):
        user = request.user
        profile = get_object_or_404(Profile, pk=profile_id)

        # 로그인하지 않은 유저, 요청한 유저와 수정할 유저 객체가 다를 경우
        if not user.is_authenticated or user != profile.user:
            return HttpResponseBadRequest()
        
        initial = self.get_initial(profile)
        form = ProfileForm(initial=initial)
        context = {
            'form': form
        }

        return render(request, 'profiles/update.html', context=context)

    # 프로필 수정 요청
    def post(self, request, profile_id):
        form = ProfileForm(request.POST, request.FILES)
        profile = get_object_or_404(Profile, pk=profile_id)

        if form.is_valid():
            profile.image = form.cleaned_data['image']
            profile.message = form.cleaned_data['message']
            profile.save()

            return redirect('profiles:mypage', user_id=request.user.pk)
        
        messages.add_message(request, messages.ERROR, '회원정보 수정에 실패하였습니다.')

        context = {
            'form': form
        }

        return render(request, 'profiles/update.html', context=context)