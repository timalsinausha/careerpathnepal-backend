from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from assessment.services.percentage_calculator import PercentageCalculatorService

from .models import AssessmentAttempt, AssessmentOption,AssessmentQuestion, StudentAnswer,OptionScore, StudentAttributeScore

from .serializers import (
    AssessmentQuestionSerializer,
    SubmitAnswerSerializer,
)
from django.db.models import Sum
from django.utils import timezone
from .services.assessment_scoring import AssessmentScoringService
from assessment.services.result_service import (
    AssessmentResultService,
)

class StartAssessmentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        student_profile = request.user.student_profile

        # Check if the student already has an unfinished attempt
        attempt = AssessmentAttempt.objects.filter(
            student=student_profile,
            is_completed=False,
        ).order_by(
            "-started_at"
        ).first()

        # If unfinished attempt exists, resume it
        if attempt:

            return Response(
                {
                    "message": (
                        "Existing assessment attempt resumed."
                    ),

                    "attempt_id": attempt.id,

                    "started_at": attempt.started_at,

                    "is_completed": attempt.is_completed,

                    "is_resumed": True,
                },

                status=status.HTTP_200_OK,
            )

        # If no unfinished attempt exists, create a new one
        attempt = AssessmentAttempt.objects.create(
            student=student_profile
        )

        return Response(
            {
                "message": (
                    "New assessment started successfully."
                ),

                "attempt_id": attempt.id,

                "started_at": attempt.started_at,

                "is_completed": attempt.is_completed,

                "is_resumed": False,
            },

            status=status.HTTP_201_CREATED,
        )

class AssessmentQuestionListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        questions = AssessmentQuestion.objects.filter(
            is_active=True
        ).prefetch_related(
            "options"
        ).order_by(
            "order"
        )

        serializer = AssessmentQuestionSerializer(
            questions,
            many=True,
        )

        return Response(
            {
                "questions": serializer.data
            },
            status=status.HTTP_200_OK,
        )
    

class SubmitAssessmentAnswerAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = SubmitAnswerSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        attempt_id = serializer.validated_data[
            "attempt_id"
        ]

        question_id = serializer.validated_data[
            "question_id"
        ]

        option_id = serializer.validated_data[
            "option_id"
        ]

        try:

            attempt = AssessmentAttempt.objects.get(
                id=attempt_id,
                student=request.user.student_profile,
                is_completed=False,
            )

        except AssessmentAttempt.DoesNotExist:

            return Response(
                {
                    "error": (
                        "Assessment attempt not found "
                        "or already completed."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            question = AssessmentQuestion.objects.get(
                id=question_id,
                is_active=True,
            )

        except AssessmentQuestion.DoesNotExist:

            return Response(
                {
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            option = AssessmentOption.objects.get(
                id=option_id,
                question=question,
            )

        except AssessmentOption.DoesNotExist:

            return Response(
                {
                    "error": (
                        "Selected option does not belong "
                        "to this question."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        answer, created = StudentAnswer.objects.update_or_create(

            attempt=attempt,

            question=question,

            defaults={
                "selected_option": option,
            },

        )

        return Response(
            {
                "message": (
                    "Answer submitted successfully."
                ),

                "answer_id": answer.id,

                "question_id": question.id,

                "selected_option": (
                    option.option_code
                ),

                "is_new_answer": created,
            },

            status=status.HTTP_200_OK,
        )
    
class CompleteAssessmentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        try:

            attempt = AssessmentAttempt.objects.get(
                id=request.data.get("attempt_id"),
                student=request.user.student_profile,
                is_completed=False,
            )

        except AssessmentAttempt.DoesNotExist:

            return Response(
                {
                    "error": (
                        "Assessment attempt not found "
                        "or already completed."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        answers = StudentAnswer.objects.filter(
            attempt=attempt
        ).select_related(
            "selected_option"
        )

        total_questions = AssessmentQuestion.objects.filter(
            is_active=True
        ).count()

        answered_questions = answers.count()

        if answered_questions != total_questions:

            return Response(
                {
                    "error": (
                        "You must answer all questions "
                        "before completing the assessment."
                    ),

                    "total_questions": total_questions,

                    "answered_questions": answered_questions,
                },

                status=status.HTTP_400_BAD_REQUEST,
            )
        attribute_scores = AssessmentScoringService(
          attempt
        ).calculate()

        # print(attribute_scores)
        for data in attribute_scores.values():

            StudentAttributeScore.objects.update_or_create(

                attempt=attempt,

                attribute=data["attribute"],

                defaults={
                    "score": data["score"],
                },

            )
            print(
                StudentAttributeScore.objects.filter(
                    attempt=attempt
                ).count()
            )

        PercentageCalculatorService.calculate(
         attempt
        )

        results= AssessmentResultService.get_results(
            attempt
        )
            

        attempt.is_completed = True

        attempt.completed_at = timezone.now()

        attempt.save(
            update_fields=[
                "is_completed",
                "completed_at",
            ]
        )

        return Response(
            {
                "has_result": True,
                "message": (
                    "Assessment completed successfully."
                ),

                "attempt_id": attempt.id,
                "completed_at": attempt.completed_at,
                "results":results,


            },

            status=status.HTTP_200_OK,

        )
    

    """
     
                 "scores": [

                    {
                        "attribute": score.attribute.name,
                        "score": score.score,
                        "percentage": score.percentage,
                    }

                    for score in StudentAttributeScore.objects.filter(
                        attempt=attempt
                    )

                 ]
                 

                 
                    "scores": [

                    {
                        "attribute": score.attribute.name,

                        "score": data[
                            "score"
                        ],
                        "percentage":data["percentage"]

                    }

                    for data in attribute_scores.values()

                ],"""
    
class AssessmentProgressAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        attempt_id = request.query_params.get(
            "attempt_id"
        )

        if not attempt_id:

            return Response(
                {
                    "error": (
                        "attempt_id is required."
                    )
                },

                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            attempt = AssessmentAttempt.objects.get(
                id=attempt_id,
                student=request.user.student_profile,
            )

        except AssessmentAttempt.DoesNotExist:

            return Response(
                {
                    "error": (
                        "Assessment attempt not found."
                    )
                },

                status=status.HTTP_404_NOT_FOUND,
            )

        total_questions = AssessmentQuestion.objects.filter(
            is_active=True
        ).count()

        answers = StudentAnswer.objects.filter(
            attempt=attempt
        ).select_related(
            "question",
            "selected_option",
        )

        answered_questions = answers.count()

        remaining_questions = (
            total_questions - answered_questions
        )

        progress_percentage = 0

        if total_questions > 0:

            progress_percentage = round(
                (
                    answered_questions
                    / total_questions
                ) * 100,

                2,
            )

        answered_data = [

            {
                "question_id": answer.question.id,

                "question_order": (
                    answer.question.order
                ),

                "selected_option_id": (
                    answer.selected_option.id
                ),

                "selected_option_code": (
                    answer.selected_option.option_code
                ),

            }

            for answer in answers

        ]

        return Response(
            {
                "attempt_id": attempt.id,

                "is_completed": (
                    attempt.is_completed
                ),

                "total_questions": (
                    total_questions
                ),

                "answered_questions": (
                    answered_questions
                ),

                "remaining_questions": (
                    remaining_questions
                ),

                "progress_percentage": (
                    progress_percentage
                ),

                "answered": answered_data,

            },

            status=status.HTTP_200_OK,
        )
    

class AssessmentResultAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Get the latest completed assessment
        attempt = (
            AssessmentAttempt.objects.filter(
                student=request.user.student_profile,
                is_completed=True,
            )
            .order_by("-completed_at")
            .first()
        )

        # If the student has never completed an assessment
        if not attempt:

            return Response(
                {
                    "has_result": False,
                    "message": "No completed assessment found.",
                },
                status=status.HTTP_200_OK,
            )

        # Generate grouped results
        results = AssessmentResultService.get_results(
            attempt
        )

        return Response(
            {
                "has_result": True,
                "attempt_id": attempt.id,
                "completed_at": attempt.completed_at,
                "results": results,
            },
            status=status.HTTP_200_OK,
        )
    
class AssessmentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        attempt = (
            AssessmentAttempt.objects
            .filter(student=request.user.student_profile)
            .order_by("-started_at")
            .first()
        )

        if attempt is None:
            return Response({
                "has_attempt": False,
                "attempt_id": None,
                "is_completed": False,
            })

        return Response({
            "has_attempt": True,
            "attempt_id": attempt.id,
            "is_completed": attempt.is_completed,
        })