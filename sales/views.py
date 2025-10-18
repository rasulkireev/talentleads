from django.contrib import messages
from django.shortcuts import redirect

from talentleads.utils import get_talentleads_logger

from .tasks import send_marketing_emails_task

logger = get_talentleads_logger(__name__)


def send_marketing_emails(request):
    message = send_marketing_emails_task()
    messages.success(request, message)
    return redirect("trigger_task")
