from django.forms import ModelForm
from profiles.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fileds = ['image', 'nickname', 'message']
