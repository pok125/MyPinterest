from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import CreateView, DetailView, ListView

from articles.models import Article
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
        article_list = Article.objects.filter(project=self.get_object())
        return super().get_context_data(object_list=article_list, **kwargs)

class ProjectList(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'