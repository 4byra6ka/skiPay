from django.urls import path

from posts.apps import PostsConfig
# from posts.views import MailingSettingsListView, MailingSettingsDetailView, MailingSettingsUpdateView, \
#     MailingSettingsDeleteView, MailingSettingsCreateView, change_is_active

app_name = PostsConfig.name

urlpatterns = [
    # path("mylist/", MailingSettingsListView.as_view(), name="my_list_send"),
    # path("mylist/create/", MailingSettingsCreateView.as_view(), name="my_list_create_send"),
    # path("mylist/<int:pk>/", MailingSettingsDetailView.as_view(), name="my_list_detail_send"),
    # path("mylist/<int:pk>/update/", MailingSettingsUpdateView.as_view(), name="my_list_update_send"),
    # path("mylist/<int:pk>/delete/", MailingSettingsDeleteView.as_view(), name="my_list_delete_send"),
    # path('mylist/<int:pk>/is_active/', change_is_active, name='change_is_active')
]
