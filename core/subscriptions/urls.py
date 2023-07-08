from django.urls import path
from .views import *

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
]
