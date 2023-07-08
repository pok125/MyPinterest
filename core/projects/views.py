from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import CreateView, DetailView, ListView

from articles.models import Article
from subscriptions.models import Subscription
from .forms import ProjectCreationForm
from .models import Project

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projects/create.html'

    def get_success_url(self):
        return reverse('projects:list')


class ProjectDetail(DetailView, MultipleObjectMixin):
    model = Project
    context_object_name = 'target_project'
    template_name = 'projects/detail.html'

    def get_context_data(self, **kwargs: Any):
        project = self.get_object()
        user = self.request.user
        article_list = Article.objects.filter(project=project)
        
        if user.is_authenticated:
            subscription = Subscription.objects.filter(user=user, project=project)
            
        return super().get_context_data(object_list=article_list, subscription=subscription, **kwargs)

class ProjectList(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'