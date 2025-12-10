import secrets
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils.models import TimeStampedModel


def generate_api_token():
    return secrets.token_urlsafe(48)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=20, blank=True)
    api_token = models.CharField(
        max_length=64,
        blank=True,
        unique=True,
        db_index=True,
        default=generate_api_token,
        help_text="API token for the user. Generated automatically when the user is created.",
    )

    class Meta:
        db_table = "auth_user"

    def regenerate_api_token(self):
        """Generate a new API token"""
        self.api_token = secrets.token_urlsafe(48)
        self.save(update_fields=["api_token"])


class OutreachTemplate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="outreach_template",
    )
    title = models.CharField(max_length=256)
    subject_line = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    cc_s = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.title


class Outreach(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outreach")
    receiver = models.ForeignKey("profiles.profile", on_delete=models.CASCADE, related_name="outreach")
    template = models.ForeignKey("OutreachTemplate", on_delete=models.CASCADE, related_name="outreach")
