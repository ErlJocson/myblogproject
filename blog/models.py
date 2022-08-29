from django.db import models
from user_authentication.models import User


class Blog(models.Model):
    title = models.CharField(max_length=24)
    content = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class BlogComment(models.Model):
    comment = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)


class AnonymousComment(models.Model):
    comment = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=24)
    email = models.CharField(max_length=24)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
