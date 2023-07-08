from typing import Any, Optional
from django import http
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import RedirectView

from projects.models import Project
from .models import Subscription

class SubscriptionView(RedirectView):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=request.GET.get('project_pk'))
        user = request.user
        subscription = Subscription.objects.filter(user=user, project=project)

        if subscription.exists():
            subscription.delete()
        else:
            Subscription.objects.create(user=user, project=project)

        return super().get(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('projects:detail', kwargs={'pk':self.request.GET.get('project_pk')})