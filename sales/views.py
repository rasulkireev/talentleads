import logging

from django.contrib import messages
from django.shortcuts import redirect

from .tasks import send_marketing_emails_task

logger = logging.getLogger(__file__)


def send_marketing_emails(request):
    message = send_marketing_emails_task()
    messages.success(request, message)
    return redirect("trigger_task")
