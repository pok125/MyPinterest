from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .decorators import ownership_required
from .forms import ArticleCreationForm
from .models import Article


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreate(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articles/create.html'

    def form_valid(self, form):
        temp_article = form.save(commit=False)
        temp_article.writer = self.request.user
        temp_article.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('articles:detail', kwargs={'pk':self.object.pk})


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'target_article'
    template_name = 'articles/detail.html'
    success_url = reverse_lazy('articles:list')


@method_decorator(ownership_required, 'get')
@method_decorator(ownership_required, 'post')
class ArticleUpdate(UpdateView):
    model = Article
    context_object_name = 'target_article'
    form_class = ArticleCreationForm
    template_name = 'articles/update.html'
    
    def get_success_url(self):
        return reverse('articles:detail', kwargs={'pk': self.object.pk})
    

@method_decorator(ownership_required, 'get')
@method_decorator(ownership_required, 'post')
class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'target_article'
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('articles:list')


class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/list.html'