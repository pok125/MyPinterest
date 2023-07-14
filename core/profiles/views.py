from django.shortcuts import render, get_object_or_404
# from django.urls import reverse, reverse_lazy
# from django.views.generic import CreateView, UpdateView
# from profiles.forms import ProfileForm
# from profiles.models import Profile
# from django.utils.decorators import method_decorator
# from profiles.decorators import ownership_required
# # Create your views here.
from django.contrib.auth import get_user_model
from django.views import View
from .models import Profile
from .forms import ProfileForm

User = get_user_model()

# class ProfileCreate(CreateView):
#     model = Profile
#     context_object_name = 'target_user'
#     form_class = ProfileForm
#     template_name = 'profiles/profile.html'
    
#     def form_valid(self, form):
#         temp_form = form.save(commit=False)
#         temp_form.user = self.request.user
#         temp_form.save()

#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse('users:mypage', kwargs={'pk': self.object.user.pk})

# @method_decorator(ownership_required, 'get')
# @method_decorator(ownership_required, 'post')
# class ProfileUpdate(UpdateView):
#     model = Profile
#     context_object_name = 'target_profile'
#     form_class = ProfileForm
#     template_name = 'profiles/update.html'
    
#     def get_success_url(self):
#         return reverse('users:mypage', kwargs={'pk': self.object.user.pk})


class ProfileView(View):
    # mypage
    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user_id=user_id)
        profile_image_url = profile.image.url if profile.image else ''
        context = {
            'target_user_profile_image_url': profile_image_url,
            'target_user_username': profile.user.username,
            'target_user_profile_message': profile.message
        }

        return render(request, 'profiles/mypage.html', context=context)