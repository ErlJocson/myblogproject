from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=24)
    content = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)


class BlogComment(models.Model):
    name = models.CharField(max_length=24)
    email = models.CharField(max_length=24)
    comment = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
