# from Will Vincent tutorial -> https://learndjango.com/tutorials/django-markdown-tutorial

import markdown as md
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

extension_configs = {
    "markdown.extensions.codehilite": {
        "css_class": "codehilite",
        "linenums": False,
        "guess_lang": False,
    }
}


@register.filter()
@stringfilter
def markdown(value):
    html = md.markdown(
        value,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.tables",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
        ],
        extension_configs=extension_configs,
    )
    return mark_safe(html)
