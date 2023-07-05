from django.http import HttpResponseForbidden
from profiles.models import Profile

def ownership_required(func):
    def decorated(request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk'])
        if not request.user == profile.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated