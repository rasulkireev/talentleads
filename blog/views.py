from django.views.generic import ListView, DetailView

from blog.models import BlogPost
from blog.choices import BlogPostStatus


class BlogView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        return BlogPost.objects.filter(status=BlogPostStatus.PUBLISHED).order_by("-created")


class BlogPostView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(status=BlogPostStatus.PUBLISHED)
