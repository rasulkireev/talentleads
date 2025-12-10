from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Display API token for a user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to show API token for")

    def handle(self, *args, **options):
        username = options["username"]

        try:
            user = User.objects.get(username=username)

            self.stdout.write(self.style.SUCCESS(f"\n{'=' * 60}"))
            self.stdout.write(self.style.SUCCESS(f"API Token for: {user.username}"))
            self.stdout.write(self.style.SUCCESS(f"{'=' * 60}\n"))
            self.stdout.write(f"Token: {user.api_token}\n")
            self.stdout.write(f"Is Superuser: {user.is_superuser}")
            self.stdout.write(f"Is Active: {user.is_active}\n")
            self.stdout.write(self.style.WARNING("Usage in cURL:"))
            self.stdout.write(
                f'  curl -H "Authorization: Bearer {user.api_token}" http://localhost:8000/api/blog/posts\n'
            )

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
