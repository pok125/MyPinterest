from django.http import HttpResponseForbidden
from .models import Article

def ownership_required(func):
    def decorated(request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        if not request.user == article.writer:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated