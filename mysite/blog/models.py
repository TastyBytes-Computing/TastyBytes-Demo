from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
import os

def rename_uploaded_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    return os.path.join('profile_images', f'{instance.user.username}.{ext}')

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

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to=rename_uploaded_image)
    bio = models.TextField(default='bio')

    def save(self, *args, **kwargs):
        # Check if this instance has already been saved (i.e., it has a primary key)
        try:
            existing = Profile.objects.get(pk=self.pk)
            if existing.avatar != self.avatar:
                # Delete the old profile picture file if it exists
                existing.avatar.delete(save=False)
        except Profile.DoesNotExist:
            pass  # New instance, nothing to delete

        # Call the parent class's save method
        super(Profile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username