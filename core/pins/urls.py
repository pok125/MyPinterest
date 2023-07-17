from django.urls import path
from .views import *

app_name = 'pins'

urlpatterns = [
    path('list', PinListView.as_view(), name='list'),
]
