from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import Home

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("pins/", include("pins.urls")),
    path("pingroups/", include("pingroups.urls")),
    path("comments/", include("comments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
