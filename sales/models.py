from django.db import models

from utils.models import BaseModel


class Email(BaseModel):
    from_email = models.EmailField()
    to_email = models.EmailField()
    reply_to_email = models.EmailField()
    subject = models.CharField(max_length=256)
    body = models.TextField(blank=True)
    replied = models.BooleanField(default=False)
