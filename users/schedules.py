from django_q.models import Schedule

schedules = [
    {
        "name": "Find HN Comments to Analyze",
        "func_path": "profiles.tasks.get_hn_pages_to_analyze",
        "hook": "profiles.hooks.print_result",
        "args": "36573869",
        "type": Schedule.DAILY,
    }
]
