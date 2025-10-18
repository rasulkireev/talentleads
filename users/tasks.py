from django.core.mail import send_mail

from talentleads.utils import get_talentleads_logger

logger = get_talentleads_logger(__name__)


def email_support_request(instance):
    message = f"""
      User: {instance["current_user"].username}
      User Email: {instance["current_user"].email}
      Message: {instance["message"]}.
    """
    send_mail(
        f"Support Request from {instance['current_user'].username}",
        message,
        "rasul@gettalentleads.com",
        ["rasul@gettalentleads.com"],
        fail_silently=False,
    )
