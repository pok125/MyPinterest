import re
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Follow

# settings에 있는 AUTH_USER_MODEL로 명시한 User사용
User = get_user_model()
email_filter = ["gmail.com", "naver.com", "nate.com", "kakao.com", "daum.net"]


class JoinForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "nickname"]
        error_messages = {
            "email": {
                "required": "이메일은 필수 입력 항목입니다.",
                "unique": "이미 사용중인 이메일입니다.",
                "invalid": "올바른 이메일 형식이 아닙니다.",
            },
            "nickname": {
                "required": "닉네임은 필수 입력 항목입니다.",
                "unique": "이미 사용중인 닉네임입니다.",
                "max_length": "닉네임은 10자 이하여야 합니다.",
            },
        }

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")

        if email.split("@")[1] not in email_filter:
            raise forms.ValidationError("사용할 수 없는 이메일입니다.")
        return email

    def clean_nickname(self) -> str:
        nickname = self.cleaned_data.get("nickname")

        if not re.match(r"^[a-zA-Z0-9가-힣]+$", nickname):
            raise forms.ValidationError(
                "닉네임은 한글, 영문자, 숫자만 사용 가능합니다."
            )
        return nickname

    def save(self) -> "User":
        cleaned_data = self.cleaned_data
        email = cleaned_data.pop("email")
        password = cleaned_data.pop("password1")
        cleaned_data.pop("password2")

        user = User.objects.create_user(email=email, password=password, **cleaned_data)
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email", "password"]


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ["from_user", "to_user"]

    def clean(self) -> dict[str, "User"]:
        cleaned_data = super().clean()
        from_user = self.cleaned_data.get("from_user")
        to_user = self.cleaned_data.get("to_user")

        if not from_user or not to_user:
            raise forms.ValidationError("팔로우할 유저를 선택해주세요.")
        if from_user == to_user:
            raise forms.ValidationError("자기 자신을 팔로우할 수 없습니다.")
        if Follow.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise forms.ValidationError("이미 팔로우한 유저입니다.")
        return cleaned_data


class MyPageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image"]
