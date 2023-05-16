import logging

import httpx
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from .models import Email
from .tasks import send_marketing_email

logger = logging.getLogger(__file__)


def get_emails(request):
    response = httpx.get(
        settings.HNJOBS_HOST + "/api/emails",
        headers={"Authorization": f"Bearer {settings.HNJOBS_API_TOKEN}"},
    )
    if response.status_code == 200:
        data = response.json()

        emails_sent = 0
        for person in data["emails"]:
            if not Email.objects.filter(to_email=person["email"]).exists():
                send_marketing_email(person)
                emails_sent += 1

        messages.success(request, f"{emails_sent} email sent.")

        return redirect("trigger_task")
