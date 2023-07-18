from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    path('create/<int:pin_id>/', CommentCreateView.as_view(), name='create'),
    path('delete/<int:comment_id>/', CommentDeleteView.as_view(), name='delete'),
]
