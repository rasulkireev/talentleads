from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Outreach, OutreachTemplate


class CustomUserAdmin(UserAdmin):
    list_display = ["date_joined", "username", "email", "first_name", "last_name"]
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {
                "fields": (
                    "twitter_handle",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Outreach)
admin.site.register(OutreachTemplate)