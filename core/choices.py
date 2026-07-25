from django.db import models


class EducationLevel(models.TextChoices):

    SEE = "SEE", "SEE"

    PLUS_TWO = "PLUS_TWO", "+2"

    DIPLOMA = "DIPLOMA", "Diploma"

    BACHELOR = "BACHELOR", "Bachelor"

    MASTER = "MASTER", "Master"

    PHD = "PHD", "PhD"


EDUCATION_ORDER = {
    EducationLevel.SEE: 1,
    EducationLevel.PLUS_TWO: 2,
    EducationLevel.DIPLOMA: 2,
    EducationLevel.BACHELOR: 3,
    }


class OwnershipType(models.TextChoices):

    PUBLIC = "PUBLIC", "Public"

    PRIVATE = "PRIVATE", "Private"

    COMMUNITY = "COMMUNITY", "Community"