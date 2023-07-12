from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.contrib import messages
from .decorators import ownership_required
from .forms import ArticleCreationForm
from .models import Article, Like
from comment.forms import CommentCreationForm


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


class ArticleDetail(DetailView, FormMixin):
    model = Article
    context_object_name = 'target_article'
    form_class = CommentCreationForm
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


class LikeArticle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('articles:detail', kwargs={'pk': kwargs['pk']})
    
    def get(self, *args, **kwargs):

        user = self.request.user
        article = get_object_or_404(Article, pk=kwargs['pk'])

        if Like.objects.filter(user=user, article=article).exists():
            messages.add_message(self.request, messages.ERROR, '좋아요는 한번만 가능합니다.')
            return redirect('articles:detail', pk=kwargs['pk'])
        else:
            Like.objects.create(user=user, article=article)
        
        article.like_count += 1
        article.save()

        messages.add_message(self.request, messages.SUCCESS, '좋아요가 반영되었습니다.')

        return super().get(self.request, *args, **kwargs)
