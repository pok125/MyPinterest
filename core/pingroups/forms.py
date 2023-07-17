from django.forms import ModelForm

from .models import PinGroup


class PinGroupCreationForm(ModelForm):

    class Meta:
        model = PinGroup
        fields = ['title', 'image', 'content']