from django.db import models
from django.db.models.base import ModelState
from users.models import User


class BlogPost(models.Model):
    """Blog post DB model"""

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="blog_post", blank=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ("-created",)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
