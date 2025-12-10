from django.contrib.syndication.views import Feed

from blog.models import BlogPost
from blog.choices import BlogPostStatus


class BlogPostFeed(Feed):
    title = "TalentLeads Blog"
    link = "/blog/"
    description = "Latest blog posts from TalentLeads"

    def items(self):
        return BlogPost.objects.filter(status=BlogPostStatus.PUBLISHED).order_by("-created")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created
