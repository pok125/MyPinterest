from django.forms import ModelForm
from .models import Pin


class PinCreationForm(ModelForm):
    
    class Meta:
        model = Pin
        fields = ['title', 'group', 'image', 'content']