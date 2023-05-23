import logging
import time

import httpx
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect

from .models import Email
from .tasks import send_marketing_email

logger = logging.getLogger(__file__)


def send_marketing_emails(request):
    response = httpx.get(
        settings.HNJOBS_HOST + "/api/emails",
        headers={"Authorization": f"Bearer {settings.HNJOBS_API_TOKEN}"},
        params={"only-approved": True},
    )
    if response.status_code == 200:
        data = response.json()

        emails_sent = 0
        email_limit = 10

        for person in data["emails"]:
            email_obj = Email.objects.filter(Q(to_email=person["email"]) & Q(failed=False))
            if not email_obj.exists():
                send_marketing_email(person)
                emails_sent += 1
                time.sleep(1)

            if emails_sent >= email_limit:
                break

        messages.success(request, f"{emails_sent} email sent.")

        return redirect("trigger_task")
