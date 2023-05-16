import logging

from django.core.mail import EmailMessage

from .models import Email

logger = logging.getLogger(__file__)


def send_marketing_email(person):
    to_email = person["email"]
    first_name = person["name"].split(" ")[0]
    from_email = "rasul@hnprofiles.email"
    subject_line = "Quick Question"
    message = f"""
Hi {first_name},

Hope your day is going well so far - just saw your post on HackerNews "Who is Hiring?" and thought I’d reach out.

I just lauhcned HN Profiles - https://hnprofiles.com - to help companies like {person['company__name']} find the most talented and qualified candidates.

There are more than 2k candidates available now and growing. The self-serve database + email outreach costs $299/month.

You can start using the tool now, but if you are interested we can do a demo call + plus discuss any questions you might have.
Let me know and I can send over a few times to chat.

Thanks, Rasul

--

Rasul Kireev | Founder
Five Greentree Centre, 525 Route 73 North STE 104 Marlton, New Jersey 08053
Mobile: 978 912 0496
rasul@hnprofiles.com
hnprofiles.com
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
