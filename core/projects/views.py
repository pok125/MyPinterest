from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from .forms import ProjectCreationForm
from .models import Project

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projects/create.html'

    def get_success_url(self):
        return reverse('projects:list')


class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'target_project'
    template_name = 'projects/detail.html'


class ProjectList(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'