from django.db import models


class CapacityChoices(models.TextChoices):
    PART_TIME_CONTRACTOR = "Part-time Contractor"
    FULL_TIME_CONTRACTOR = "Full-time Contractor"
    PART_TIME_EMPLOYEE = "Part-time Employee"
    FULL_TIME_EMPLOYEE = "Full-time Employee"


class LevelChoices(models.TextChoices):
    SENIOR = "Senior"
    MID_LEVEL = "Mid-level"
    JUNIOR = "Junior"
    PRINCIPAL = "Principal"
    C_LEVEL = "C-Level"
