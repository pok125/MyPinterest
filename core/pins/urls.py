from django.urls import path
from .views import *

app_name = 'pins'

urlpatterns = [
    path('list', PinListView.as_view(), name='list'),
    path('create', PinCreateView.as_view(), name='create'),
    path('detail/<int:pin_id>', PinDetailView.as_view(), name='detail'),
    path('update/<int:pin_id>', PinUpdateView.as_view(), name='update'),
    path('delete/<int:pin_id>', PinDeleteView.as_view(), name='delete'),
]
