from django.urls import path
from .views import *

app_name = 'pingroups'

urlpatterns = [
    path('list', PinGroupListView.as_view(), name='list'),
    path('create', PinGroupCreateView.as_view(), name='create'),
    path('detail/<int:pingroup_id>', PinGroupDetailView.as_view(), name='detail'),
    path('update/<int:pingroup_id>', PinGroupUpdateView.as_view(), name='update'),
]
