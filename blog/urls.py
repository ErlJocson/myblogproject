from django.urls import path
from .views import *

urlpatterns = [
    path("get-blog/<int:id>", get_blog),
    path("get-blogs/", get_blogs),
    path("add-blog/", add_blog),
    path("delete-blog/<int:id>", delete_blog),
    path("update-blog/<int:id>", update_blog),

    path("get-comments/<int:blog_id>", get_comments),
    path("delete-comment/<int:id>", delete_comment),
    path("update-comment/<int:id>", update_comment)
]