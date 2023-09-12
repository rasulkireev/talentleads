import logging

import httpx
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q
from django_q.tasks import async_task

from .models import Email

logger = logging.getLogger(__file__)


def send_marketing_emails_task():
    response = httpx.get(
        settings.HNJOBS_HOST + "/api/emails",
        headers={"Authorization": f"Bearer {settings.HNJOBS_API_TOKEN}"},
        params={"only-approved": True},
    )
    status_code = response.status_code
    logger.info(f"Getting Emails... Result: {status_code}")

    if status_code == 200:
        data = response.json()

        emails_sent = 0
        email_limit = 10

        for person in data["emails"]:
            email_obj = Email.objects.filter(Q(to_email=person["email"]) & Q(failed=False))
            if not email_obj.exists():
                async_task(send_marketing_email, person, hook="profiles.hooks.print_result", group="Sales")
                emails_sent += 1

            if emails_sent >= email_limit:
                break

        return f"{emails_sent} emails will be sent."

    return "Something went wrong"


def send_marketing_email(person):
    to_email = person["email"]
    first_name = person["name"].split(" ")[0]
    from_email = "Rasul Kireev <rasul@gettalentleads.com>"
    subject_line = "Quick Question"
    message = f"""
Hi {first_name},

I saw on HackerNews that you are hiring at {person['company__name']}.
Can I ask you a few questions about your hiring process?

Best,
Rasul
    """  # noqa E501

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

    logger.info(f"Sent email to {first_name}: {to_email}")


serious_message = """
Hi {first_name},

Hope your day is going well so far - just saw your post on HackerNews "Who is Hiring?" and thought I’d reach out.

I just lauhcned TalentLeads - https://gettalentleads.com - to help companies like {person['company__name']} find the most talented and qualified candidates.

There are more than 2k candidates available now and growing. The self-serve database + email outreach costs $299/month.

You can start using the tool now, but if you are interested we can do a demo call + plus discuss any questions you might have.
Let me know and I can send over a few times to chat.

Thanks, Rasul

--

Rasul Kireev | Founder
Five Greentree Centre, 525 Route 73 North STE 104 Marlton, New Jersey 08053
Mobile: 978 912 0496
rasul@gettalentleads.com
gettalentleads.com
"""  # noqa E501
