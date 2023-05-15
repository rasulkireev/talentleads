import logging

from django.core.mail import EmailMessage

from .models import Email

logger = logging.getLogger(__file__)


def send_marketing_email(person):
    to_email = person["email"]
    from_email = "rasul@hnprofiles.email"
    subject_line = "Quick Question"
    message = f"""
    Email: {to_email}
    Name: {person['name']}
    """

    logger.info(f"message: {message}")

    email = Email(
        from_email=from_email,
        to_email=to_email,
        reply_to_email=from_email,
        subject=subject_line,
        body=message,
    )
    email.save()

    email = EmailMessage(subject=subject_line, body=message, from_email=from_email, to=[to_email])

    email.send(fail_silently=True)
