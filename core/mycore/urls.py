from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from articles.views import ArticleListView


urlpatterns = [
    path('', ArticleListView.as_view()),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('profiles/', include('profiles.urls')),
    path('articles/', include('articles.urls')),
    path('comment/', include('comment.urls')),
    path('projects/', include('projects.urls')),
    path('subscriptions/', include('subscriptions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
