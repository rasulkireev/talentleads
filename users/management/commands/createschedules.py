from django.core.management.base import BaseCommand
from django_q.models import Schedule

from talentleads.utils import get_talentleads_logger
from users.schedules import schedules

logger = get_talentleads_logger(__name__)


class Command(BaseCommand):
    help = "Create django_q schedules"

    def handle(self, *args, **options):
        for schedule in schedules:
            if not Schedule.objects.filter(name=schedule["name"]).exists():
                Schedule.objects.create(
                    func=schedule["func_path"],
                    name=schedule["name"],
                    hook=schedule["hook"],
                    args=schedule["args"],
                    schedule_type=schedule["type"],
                    cron=schedule["cron"],
                )
                logger.info(f"Schedule `{schedule['name']}` is created.")
            else:
                logger.info(f"Schedule `{schedule['name']}` already exists.")
