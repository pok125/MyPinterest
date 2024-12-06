from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import FollowForm, JoinForm, LoginForm, MyPageUpdateForm
from .models import Follow

User = get_user_model()


### Join
class JoinView(View):
    # 회원가입 페이지
    def get(self, request):
        user = request.user

        # 이미 로그인 한 상태인 유저
        if user.is_authenticated:
            messages.add_message(request, messages.ERROR, "로그아웃 후 진행해 주세요.")
            return redirect("/")

        form = JoinForm()
        context = {"form": form}

        return render(request, "users/join.html", context=context)

    # 회원가입 요청
    def post(self, request):
        form = JoinForm(request.POST)

        # form 유효성 검사
        if form.is_valid():
            try:
                form.save()
                return redirect("users:login")
            except Exception as e:
                print(f"에러발생{e}")
                messages.add_message(request, messages.ERROR, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Form Error - {field}: {error}")
            messages.add_message(request, messages.ERROR, "회원가입에 실패하였습니다.")

        context = {"form": form}
        return render(request, "users/join.html", context=context)


### Login
class LoginView(View):
    # 로그인 페이지
    def get(self, request):
        user = request.user

        # 이미 로그인된 유저
        if user.is_authenticated:
            messages.add_message(request, messages.ERROR, "이미 로그인된 상태입니다.")
            return redirect("/")

        form = LoginForm()
        context = {"form": form}

        return render(request, "users/login.html", context=context)

    # 로그인 요청
    def post(self, request):
        form = LoginForm(request, request.POST)

        # form 유효성 검사
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)

            # 해당 입력 정보에 대한 유저검사
            if user:
                login(request, user)
                return redirect("/")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Form Error - {field}: {error}")
                    messages.add_message(request, messages.ERROR, f"{error}")

        context = {"form": form}
        return render(request, "users/login.html", context=context)


### Logout
class LogoutView(View):
    # 로그아웃 요청
    def get(self, request):
        logout(request)
        return redirect("/")


### UserDelete
class UserDeleteView(LoginRequiredMixin, View):
    # 회원탈퇴 요청
    def post(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(User, pk=user_id)

        if user != target_user:
            return HttpResponseBadRequest()

        target_user.delete()

        return redirect("home")


### Following
class FollowingView(LoginRequiredMixin, View):
    # 팔로우 요청
    def get(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(User, pk=user_id)
        form_data = {"from_user": user, "to_user": target_user}
        form = FollowForm(data=form_data)

        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print(f"에러발생{e}")
                messages.add_message(request, messages.ERROR, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Form Error - {field}: {error}")
            messages.add_message(request, messages.ERROR, "팔로우에 실패하였습니다.")

        return redirect("users:mypage", user_id=target_user.id)


### UnFollowing
class UnFollowingView(LoginRequiredMixin, View):
    # 팔로우 취소
    def get(self, request, user_id):
        user = request.user
        target_user = get_object_or_404(User, pk=user_id)
        follow_record = Follow.objects.filter(from_user=user, to_user=target_user)

        if follow_record.exists():
            follow_record.delete()
        return redirect("users:mypage", user_id=target_user.id)


### MyPage
class MyPageView(View):
    # mypage
    def get(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        user = request.user
        is_following = False

        if (
            not user.is_anonymous
            and Follow.objects.filter(from_user=user, to_user=target_user).exists()
        ):
            is_following = True

        pin_count = target_user.pin.count()
        following_count = target_user.followers_count

        context = {
            "target_user": target_user,
            "user": user,
            "pin_count": pin_count,
            "following_count": following_count,
            "is_following": is_following,
        }

        return render(request, "users/mypage.html", context=context)


### UserUpdate
class MyPageUpdateView(LoginRequiredMixin, View):
    # form에 대한 초기 값 세팅을 위해 initial객체 사용
    def get_initial(self, user):
        initial = dict()
        initial["image"] = user.image
        initial["message"] = user.message

        return initial

    # 프로필 수정 페이지
    def get(self, request):
        user = request.user
        initial = self.get_initial(user)
        form = MyPageUpdateForm(initial=initial)
        context = {"form": form}

        return render(request, "users/update.html", context=context)

    # 프로필 수정 요청
    def post(self, request):
        user = request.user
        form = MyPageUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            user.image = form.cleaned_data["image"]
            user.message = form.cleaned_data["message"]
            user.save()
            return redirect("users:mypage", user_id=user.id)
        else:
            messages.add_message(
                request, messages.ERROR, "회원정보 수정에 실패하였습니다."
            )
            context = {"form": form}
            return render(request, "users/update.html", context=context)
