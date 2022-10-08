from django.contrib import admin
from .models import Blog, BlogComment, Vote

admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(Vote)