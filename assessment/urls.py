from django.urls import path

from .views import (
    AssessmentResultAPIView,
    StartAssessmentAPIView,
    AssessmentQuestionListAPIView,
    SubmitAssessmentAnswerAPIView,
    CompleteAssessmentAPIView,
    AssessmentProgressAPIView,
    AssessmentStatusAPIView
)


urlpatterns = [
# POST http://127.0.0.1:8000/api/assessment/start/
    path(
        "start/",
        StartAssessmentAPIView.as_view(),
        name="start-assessment",
    ),

# GET http://127.0.0.1:8000/api/assessment/questions/
     path(
        "questions/",
        AssessmentQuestionListAPIView.as_view(),
        name="assessment-questions",
    ),
#POST http://127.0.0.1:8000/api/assessment/answer/
    path(
    "answer/",
    SubmitAssessmentAnswerAPIView.as_view(),
    name="submit-assessment-answer",
    ),

    #POST http://127.0.0.1:8000/api/assessment/complete/
    path(
        "complete/",
        CompleteAssessmentAPIView.as_view(),
        name="complete-assessment",
    ),
# GET http://127.0.0.1:8000/api/assessment/progress/?attempt_id=1
    path(
    "progress/",
    AssessmentProgressAPIView.as_view(),
    name="progress-assessment"
    ),
#GET http://127.0.0.1:8000/api/assessment/result/
    path(
    "result/",
    AssessmentResultAPIView.as_view(),
    name="assessment-result",
    ),
    
    #GET http://127.0.0.1:8000/api/assessment/status/
    path(
    "status/",
    AssessmentStatusAPIView.as_view(),
    name="assessment-status",
),


]