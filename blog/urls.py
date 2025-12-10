from django.urls import path

from blog import views
from blog.feeds import BlogPostFeed

urlpatterns = [
    path("", views.BlogView.as_view(), name="blog_posts"),
    path("feed/", BlogPostFeed(), name="blog_feed"),
    path("<slug:slug>/", views.BlogPostView.as_view(), name="blog_post"),
]
