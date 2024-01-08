from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from .utils import get_garavatar_url


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        context = super().get_context(request)
        blog_pages = self.get_children().live().order_by("-first_published_at")
        context["blog_pages"] = blog_pages

        return context


class BlogPage(Page):
    date_created = models.DateField("Created Date")
    date_modified = models.DateField("Modified Date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    icon = models.ForeignKey("wagtailimages.Image", on_delete=models.PROTECT, related_name="+")
    main_image = models.ForeignKey("wagtailimages.Image", on_delete=models.PROTECT, related_name="+")

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date_created"),
                FieldPanel("date_modified"),
                FieldPanel("intro"),
                FieldPanel("icon"),
            ],
            heading="Post Info",
        ),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["gravatar_url"] = get_garavatar_url(self.owner.email)

        return context
