from assessment.models import (
    AssessmentAttribute,
    StudentAttributeScore,
)


class AssessmentResultService:

    @staticmethod
    def get_results(attempt):

        grouped_results = {
            "interest": [],
            "trait": [],
            "work_style": [],
            "value": [],
            "aptitude": [],
        }

        student_scores = {
            score.attribute_id: score
            for score in StudentAttributeScore.objects.filter(
                attempt=attempt
            )
        }

        attributes = AssessmentAttribute.objects.filter(
            is_active=True
        )

        for attribute in attributes:

            student_score = student_scores.get(
                attribute.id
            )

            if student_score:

                result = {
                    "attribute": attribute.name,
                    "score": student_score.score,
                    "percentage": float(
                        student_score.percentage
                    ),
                }

            else:

                result = {
                    "attribute": attribute.name,
                    "code": attribute.code,
                    "score": student_score.score,
                    "percentage": float(student_score.percentage),
                }

            grouped_results[
                attribute.category.lower()
            ].append(result)

        for category in grouped_results.values():

            category.sort(
                key=lambda item: item["percentage"],
                reverse=True,
            )

        return grouped_results