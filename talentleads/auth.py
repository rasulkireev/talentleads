from ninja.security import HttpBearer
from django.contrib.auth import get_user_model

from talentleads.utils import get_talentleads_logger

logger = get_talentleads_logger(__name__)
User = get_user_model()


class TokenAuth(HttpBearer):
    """
    Token-based authentication for Django Ninja API.

    Usage:
        Add header: Authorization: Bearer your_api_token_here
    """

    def authenticate(self, request, token: str):
        try:
            user = User.objects.get(api_token=token)
            logger.info(
                "Token authentication successful",
                username=user.username,
                is_superuser=user.is_superuser,
                is_staff=user.is_staff,
            )
            return user
        except User.DoesNotExist:
            logger.warning("Token authentication failed - user not found")
            return None
