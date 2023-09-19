from django.urls import path

from posts.apps import PostsConfig
from posts.views import PostMyListView, PostMyDetailView, PostMyUpdateView, PostMyDeleteView, PostMyCreateView, \
    PostListView, PostFreeDetailView, PostPayRedirectView

app_name = PostsConfig.name

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
    path("free/<int:pk>/", PostFreeDetailView.as_view(), name="free_posts_detail"),
    path("pay/<int:pk>/", PostPayRedirectView.as_view(), name="pay_posts_redirect"),
    path("mylist/", PostMyListView.as_view(), name="my_posts"),
    path("mylist/create/", PostMyCreateView.as_view(), name="my_posts_create"),
    path("mylist/<int:pk>/", PostMyDetailView.as_view(), name="my_posts_detail"),
    path("mylist/<int:pk>/update/", PostMyUpdateView.as_view(), name="my_posts_update"),
    path("mylist/<int:pk>/delete/", PostMyDeleteView.as_view(), name="my_posts_delete"),
]
