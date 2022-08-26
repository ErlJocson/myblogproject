from django.urls import path
from .views import *

urlpatterns = [
    path("get-blog/<int:id>", get_blog),
    path("get-blogs/", get_blogs),
    path("get-comments/", get_comments),
    path("add-blog/", add_blog),
    path("delete-blog/<int:id>", delete_blog),
    path("update-blog/<int:id>", update_blog),
]