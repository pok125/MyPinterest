from django.urls import path
from .views import *

app_name = 'articles'

urlpatterns = [
    # path('list/', ArticleListView.as_view(), name='list'),
    # path('create/', ArticleCreate.as_view(), name='create'),
    # path('detail/<int:pk>', ArticleDetail.as_view(), name='detail'),
    # path('update/<int:pk>', ArticleUpdate.as_view(), name='update'),
    # path('delete/<int:pk>', ArticleDelete.as_view(), name='delete'),
    # path('like/<int:pk>', LikeArticle.as_view(), name='like'),
]
