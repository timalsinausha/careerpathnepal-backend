from django.core.management.base import BaseCommand
from django.db import transaction

from assessment.models import (
    AssessmentAttribute,
    AssessmentQuestion,
    AssessmentOption,
    OptionScore,
)

from assessment.data.assessment_attributes import ATTRIBUTES
from assessment.data.assessment_data import ASSESSMENT_DATA

print("Questions:", len(ASSESSMENT_DATA))


class Command(BaseCommand):

    help = "Seed assessment data"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(
            self.style.NOTICE(
                "Seeding assessment data..."
            )
        )

        # ==========================================
        # Seed Attributes
        # ==========================================

        for attribute_data in ATTRIBUTES:

            AssessmentAttribute.objects.update_or_create(

                code=attribute_data["code"],

                defaults={
                    "name": attribute_data["name"],
                    "category": attribute_data["category"],
                },

            )

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Attributes seeded."
            )
        )

        # ==========================================
        # Seed Questions, Options and Scores
        # ==========================================

        for question_data in ASSESSMENT_DATA:

            question, _ = AssessmentQuestion.objects.update_or_create(

                order=question_data["order"],

                defaults={

                    "section": question_data["section"],

                    "question_text": question_data["question_text"],

                    "is_active": True,

                },

            )

            for index, option_data in enumerate(
                question_data["options"],
                start=1,
            ):

                option, _ = AssessmentOption.objects.update_or_create(

                    question=question,

                    option_code=option_data["code"],

                    defaults={

                        "option_text": option_data["text"],

                        "order": index,

                        "is_correct": option_data.get(
                            "is_correct",
                            False,
                        ),

                    },

                )

                attribute = AssessmentAttribute.objects.get(

                    code=option_data["attribute_code"]

                )

                OptionScore.objects.update_or_create(

                    option=option,

                    attribute=attribute,

                    defaults={

                        "score": option_data.get(
                            "score",
                            1,
                        ),

                    },

                )

        self.stdout.write("")

        self.stdout.write(

            self.style.SUCCESS(
                "======================================"
            )

        )

        self.stdout.write(

            self.style.SUCCESS(
                " Assessment seeded successfully!"
            )

        )

        self.stdout.write(

            self.style.SUCCESS(
                "======================================"
            )

        )