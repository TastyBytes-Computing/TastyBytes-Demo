from django.shortcuts import render
from django.views.generic.base import TemplateView
from . import models

class HomeView(TemplateView):
    """views for the home.html"""
    template_name = "blog/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = models.Post.objects.order_by('updated').reverse()
        context.update(
            {
                'latest_posts' : latest_posts
            }
        )
        return context