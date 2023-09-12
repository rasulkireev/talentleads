import json
import logging
import re

import httpx
import openai
from django.conf import settings
from django.core.mail import EmailMessage
from django_q.tasks import async_task

from .models import Profile, Technology
from .utils import clean_profile_json_object

# from django_q.models import Schedule


logger = logging.getLogger(__file__)
openai.api_key = settings.OPENAI_KEY


def get_hn_pages_to_analyze(who_wants_to_be_hired_post_id):
    data = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{who_wants_to_be_hired_post_id}.json").json()

    if "Who wants to be hired" not in data["title"]:
        return "Not a Who wants to be hired"

    list_of_comment_ids = data["kids"]

    # if working in dev don't want to go through all the comments
    if settings.DEBUG:
        list_of_comment_ids = list_of_comment_ids[:150]

    count = 0
    for comment_id in list_of_comment_ids:
        if not Profile.objects.filter(who_wants_to_be_hired_comment_id=comment_id).exists():
            async_task(
                analyze_hn_page,
                data,
                comment_id,
                hook="profiles.hooks.print_result",
                group="Analyze HN Page",
            )
            count += 1
        else:
            logger.info(f"Profile for {comment_id} already exists.")

    return f"{count} have been sent to be analyzed."


def analyze_hn_page(orig_data, comment_id):
    who_wants_to_be_hired_id = int(orig_data["id"])
    who_wants_to_be_hired_title = str(re.search("\(([^)]+)", orig_data["title"]).group(1))

    logger.info(f"Analyzing comment {comment_id}")
    json_profile = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json").json()

    try:
        if json_profile["deleted"] is True:
            return "Comment was deleted"
    except KeyError:
        pass

    who_wants_to_be_hired_comment_id = int(json_profile["id"])
    hn_username = str(json_profile["by"])

    logger.info(f"JSON for comment {comment_id}: {json_profile}")

    request = f"""Convert the text below into json object with the following valid keys (give me an empty string if there is no info, ignore the content in  brackets, it is only to explain what I need):
        - location (can't be empty)
        - city (figure out from location, can't be empty)
        - country (figure out from location, can't be empty)
        - state (if country is USA please guess the state, otherwise empty string. keep the short format, like MA, NY, etc.)
        - is_remote (boolean)
        - willing_to_relocate (choose from: Yes, No, Maybe. can't be empty)
        - technologies_used (string of comma separated values. split values like HTML/CSS into HTML, CSS)
        - resume_link (valid url or empty)
        - email (valid email or empty)
        - personal_website (valid url or empty)
        - description (can't be empty)
        - name (Full Name if mentioned)
        - title (come up with a short - 6 words max - title based on one of the technologies_used and description, can't be empty)
        - level (choose from these options: Junior, Mid-level, Senior, Principal, C-Level. figure out from description, can't be empty)
        - years_of_experience (figure out from description, make a best guess, can't be empty. make sure this is an integer, so no values like 40+, only 40)
        - capacity (string of comma separated values. options are 'Part-time Contractor', 'Full-time Contractor', 'Part-time Employee' and 'Full-time Employee', can't be empty)

        Don't add any text and only respond with a JSON Object.

        Text: '''
        {json_profile['text']}
        '''
    """  # noqa: E501

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": request},
            ],
        )
        logger.info(f"Got Completion for {comment_id}")
        converted_comment_response = completion.choices[0].message
    except (openai.error.RateLimitError, openai.error.APIError) as e:
        return logger.error(e)

    try:
        json_converted_comment_response = json.loads(converted_comment_response.content)
    except json.decoder.JSONDecodeError:
        return "Data was not in the JSON format"

    cleaned_data = clean_profile_json_object(json_profile, json_converted_comment_response)

    technology_names = [name.strip() for name in cleaned_data["technologies_used"].split(",")]
    technologies = []
    for name in technology_names:
        if name != "":
            obj, _ = Technology.objects.get_or_create(name=name)
            technologies.append(obj)

    profile = Profile(
        latest_who_wants_to_be_hired_id=who_wants_to_be_hired_id,
        who_wants_to_be_hired_title=who_wants_to_be_hired_title,
        who_wants_to_be_hired_comment_id=who_wants_to_be_hired_comment_id,
        title=cleaned_data["title"],
        name=cleaned_data["name"],
        hn_username=hn_username,
        description=cleaned_data["description"],
        location=cleaned_data["location"],
        city=cleaned_data["city"],
        country=cleaned_data["country"],
        state=cleaned_data["state"],
        level=cleaned_data["level"],
        is_remote=cleaned_data["is_remote"],
        willing_to_relocate=cleaned_data["willing_to_relocate"],
        resume_link=cleaned_data["resume_link"],
        personal_website=cleaned_data["personal_website"],
        email=cleaned_data["email"],
        years_of_experience=cleaned_data["years_of_experience"],
        capacity=cleaned_data["capacity"],
    )
    profile.save()
    profile.tech_stack.add(*technologies)

    logger.info(f"{profile} profile was created.")

    return "Task Completed"


# Schedule.objects.create(
#     func=analyze_hn_page,
#     args=34983765,
#     hook="hooks.print_result",
#     schedule_type=Schedule.CRON,
#     cron = '0 0 * * *'
# )


def send_outreach_email_task(subject_line, message, receiver, user, send_to_list):
    cc_s = [email.strip() for email in send_to_list.split(",") if send_to_list] + [user.email]
    logger.info(f"Sending email to {receiver} with cc {cc_s}")
    email = EmailMessage(
        subject=subject_line,
        body=message,
        from_email="Rasul Kireev <rasul@gettalentleads.com>",
        to=[receiver],
        reply_to=[user.email],
        cc=cc_s,
    )
    email.send(fail_silently=True)
