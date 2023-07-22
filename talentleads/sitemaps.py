from django.contrib import sitemaps
from django.contrib.sitemaps import GenericSitemap
from django.urls import reverse

from profiles.models import Profile


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5

    def items(self):
        return [
            "home",
            "profiles",
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    "sitemaps": {
        "static": StaticViewSitemap,
        "profiles": GenericSitemap(
            {
                "queryset": Profile.objects.all(),
                "date_field": "modified",
            }
        ),
    }
}
