from django.contrib import admin
from django.db import models
from django.forms import Textarea

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "created", "modified"]
    list_filter = ["status", "created"]
    search_fields = ["title", "description", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created"
    ordering = ["-created"]

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 80})},
    }

    fieldsets = (
        ("Content", {"fields": ("title", "slug", "description", "content")}),
        ("Metadata", {"fields": ("tags", "status")}),
        ("Media", {"fields": ("icon", "image"), "classes": ("collapse",)}),
    )
