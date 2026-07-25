from decimal import Decimal

from django.db.models import Max

from assessment.models import (
    StudentAttributeScore,
    OptionScore,
)


class PercentageCalculatorService:

    @staticmethod
    def calculate(attempt):

        student_scores = StudentAttributeScore.objects.filter(
            attempt=attempt
        )

        for student_score in student_scores:

            attribute = student_score.attribute


            max_possible_score = 0


            option_scores = (
                OptionScore.objects
                .filter(
                    attribute=attribute
                )
                .select_related(
                    "option",
                    "option__question"
                )
            )


            question_max_scores = {}


            for option_score in option_scores:

                question_id = (
                    option_score
                    .option
                    .question
                    .id
                )

                current_score = (
                    question_max_scores
                    .get(question_id, 0)
                )


                if option_score.score > current_score:

                    question_max_scores[
                        question_id
                    ] = option_score.score



            max_possible_score = sum(
                question_max_scores.values()
            )


            if max_possible_score == 0:

                student_score.percentage = 0

            else:

                percentage = (
                    Decimal(student_score.score)
                    /
                    Decimal(max_possible_score)
                ) * 100


                student_score.percentage = round(
                    percentage,
                    2
                )


            student_score.save()


        return student_scores