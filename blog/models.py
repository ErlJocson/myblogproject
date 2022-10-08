from django.db import models
from user_authentication.models import User


class Blog(models.Model):
    title = models.CharField(max_length=24)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BlogComment(models.Model):
    content = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
