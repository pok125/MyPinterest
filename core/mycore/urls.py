from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from .views import Home

urlpatterns = [
    path('', Home.as_view()),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('profiles/', include('profiles.urls')),
    path('pins/', include('pins.urls')),
    path('pingroups/', include('pingroups.urls')),
    path('projects/', include('projects.urls')),
    path('subscriptions/', include('subscriptions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
