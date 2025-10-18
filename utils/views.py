import logging

from allauth.account.models import EmailAddress
from django.db.utils import IntegrityError
from djstripe.models import Customer, Subscription

from talentleads.utils import get_talentleads_logger

logger = get_talentleads_logger(__name__)


def add_users_context(context, user):
    try:
        customer = Customer.objects.get(subscriber=user)
        logger.info(f"Adding customer {customer} to context (id: {customer.id}).")
        context["customer"] = customer

        try:
            subscription = Subscription.objects.get(customer=customer)
            logger.info(f"Adding subscription {subscription} to context.")
            context["subscription"] = subscription
        except Subscription.DoesNotExist:
            pass

    except (Customer.DoesNotExist, IntegrityError):
        customer = Customer.create(subscriber=user)
        logging.info(f"Created User: {customer}")

    try:
        context["email_verified"] = EmailAddress.objects.get_for_user(user, user.email).verified
    except EmailAddress.DoesNotExist:
        logger.error("User doesn't have a Verfiied Email")

    return context
