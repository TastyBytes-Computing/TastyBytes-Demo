from django.contrib import admin
from .models import Post, Topic, Profile


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug':('name',)}

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'created',
        'updated',
        'status'
    )
admin.site.register(Post, PostAdmin)

admin.site.register(Profile)