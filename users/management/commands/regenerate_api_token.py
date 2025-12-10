from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Regenerate API token for a user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to regenerate API token for")

    def handle(self, *args, **options):
        username = options["username"]

        try:
            user = User.objects.get(username=username)
            old_token = user.api_token
            user.regenerate_api_token()

            self.stdout.write(self.style.SUCCESS(f"\n{'=' * 60}"))
            self.stdout.write(self.style.SUCCESS(f"API Token Regenerated for: {user.username}"))
            self.stdout.write(self.style.SUCCESS(f"{'=' * 60}\n"))
            self.stdout.write(self.style.WARNING(f"Old Token: {old_token}"))
            self.stdout.write(self.style.SUCCESS(f"New Token: {user.api_token}\n"))

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
