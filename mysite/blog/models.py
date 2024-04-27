from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = self.model.PUBLISHED)
    def draft(self):
        return self.filter(status = self.model.DRAFT)

class Topic(models.Model):
    name = models.CharField(
        max_length = 50,
        unique = True
    )
    slug = models.SlugField(unique = True)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    """represents a blog post"""
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    title = models.CharField(max_length = 255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete = models.PROTECT,
        related_name = 'blog_posts',
        null = True,
    )
    status = models.CharField(
        max_length = 10,
        choices = STATUS_CHOICES,
        default = DRAFT,
        help_text = 'Set to "published" to make this post be publicly seen'
    )
    topics = models.ManyToManyField(
        Topic, 
        related_name = "blog_posts"
    )
    def __str__(self):
        return self.title
    
    objects = PostQuerySet.as_manager()


