from typing import Any

from django.forms import ModelForm, ValidationError

from .models import BookMark, LikeRecord, Pin


class PinCreationForm(ModelForm):

    class Meta:
        model = Pin
        fields = ["title", "group", "image", "content"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = user.pingroup.all()


class CheckLikeForm(ModelForm):
    class Meta:
        model = LikeRecord
        fields = ["pin", "user"]

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        user = cleaned_data.get("user")

        if not pin or not user:
            raise ValidationError("Pin 또는 유저를 선택해주세요.")
        if pin.writer == user:
            raise ValidationError("자신의 Pin에는 좋아요를 누를 수 없습니다.")

        return cleaned_data


class CheckBookMarkForm(ModelForm):
    class Meta:
        model = BookMark
        fields = ["pin", "user"]

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        user = cleaned_data.get("user")

        if not pin or not user:
            raise ValidationError("Pin 또는 유저를 선택해주세요.")
        if pin.writer == user:
            raise ValidationError("자신의 Pin에는 즐겨찾기를 할 수 없습니다.")

        return cleaned_data
