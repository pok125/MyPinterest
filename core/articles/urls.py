from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'articles'

urlpatterns = [
    path('list/', TemplateView.as_view(template_name='articles/list.html'), name='list'),
    path('create/', ArticleCreate.as_view(), name='create'),
    path('detail/<int:pk>', ArticleDetail.as_view(), name='detail'),
    path('update/<int:pk>', ArticleUpdate.as_view(), name='update'),
    path('delete/<int:pk>', ArticleDelete.as_view(), name='delete'),
]
