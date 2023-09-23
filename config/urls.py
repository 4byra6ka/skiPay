from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
