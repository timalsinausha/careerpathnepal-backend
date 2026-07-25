from rest_framework import serializers

from .models import (
    AssessmentQuestion,
    AssessmentOption,
)


class AssessmentOptionSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = AssessmentOption

        fields = [
            "id",
            "option_code",
            "option_text",
            "order",
        ]


class AssessmentQuestionSerializer(
    serializers.ModelSerializer
):

    options = AssessmentOptionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = AssessmentQuestion

        fields = [
            "id",
            "order",
            "question_text",
            "options",
        ]
        

class SubmitAnswerSerializer(
    serializers.Serializer
):

    attempt_id = serializers.IntegerField()

    question_id = serializers.IntegerField()

    option_id = serializers.IntegerField()