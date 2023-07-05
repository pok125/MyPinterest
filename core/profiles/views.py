from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from profiles.forms import ProfileForm
from profiles.models import Profile
from django.utils.decorators import method_decorator
from profiles.decorators import ownership_required
# Create your views here.

class ProfileCreate(CreateView):
    model = Profile
    context_object_name = 'target_user'
    form_class = ProfileForm
    template_name = 'profiles/profile.html'
    
    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.user = self.request.user
        temp_form.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('users:mypage', kwargs={'pk': self.object.user.pk})

@method_decorator(ownership_required, 'get')
@method_decorator(ownership_required, 'post')
class ProfileUpdate(UpdateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileForm
    template_name = 'profiles/update.html'
    
    def get_success_url(self):
        return reverse('users:mypage', kwargs={'pk': self.object.user.pk})