from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from profiles.forms import ProfileForm

from profiles.models import Profile
# Create your views here.

class ProfileCreate(CreateView):
    model = Profile
    context_object_name = 'target_user'
    form_class = ProfileForm
    template_name = 'profiles/profile.html'
    success_url = reverse_lazy('users:test')

    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.user = self.request.user
        temp_form.save()

        return super().form_valid(form)