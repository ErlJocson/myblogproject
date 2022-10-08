from django.urls import path
from .views import *

# TODO: add the new views to the url patterns
urlpatterns = [
    path("get-blog/<int:blog_id>", get_blog),
    path("get-blogs/", get_blogs),
    path("add-blog/", add_blog),
    path("delete-blog/<int:blog_id>", delete_blog),
    path("update-blog/<int:blog_id>", update_blog),

    path("get-comments/<int:blog_id>", get_comments),
    path("delete-comment/<int:comment_id>", delete_comment),
    path("update-comment/<int:comment_id>", update_comment),
    path("add-comment/", add_comment),
]