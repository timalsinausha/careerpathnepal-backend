from django.db import transaction

from assessment.models import (
    StudentAnswer,
    OptionScore,
    StudentAttributeScore,
    AssessmentAttribute
)


class AssessmentScoringService:

    def __init__(self, attempt):
        self.attempt = attempt

    @transaction.atomic
    def calculate(self):

        answers = StudentAnswer.objects.filter(
            attempt=self.attempt
        ).select_related(
            "selected_option"
        )

        # attribute_scores = {}
        attribute_scores = {
            attribute.id: {
                "attribute": attribute,
                "score": 0,
            }
            for attribute in AssessmentAttribute.objects.filter(
                is_active=True
            )
        }

        for answer in answers:

            option_scores = OptionScore.objects.filter(
                option=answer.selected_option
            ).select_related(
                "attribute"
            )

            for option_score in option_scores:

                attribute_id = option_score.attribute.id

                if attribute_id not in attribute_scores:

                    attribute_scores[attribute_id] = {
                        "attribute": option_score.attribute,
                        "score": 0,
                    }

                attribute_scores[attribute_id]["score"] += (
                    option_score.score
                )

        for data in attribute_scores.values():

            StudentAttributeScore.objects.update_or_create(

                attempt=self.attempt,

                attribute=data["attribute"],

                defaults={
                    "score": data["score"],
                },

            )

        return attribute_scores