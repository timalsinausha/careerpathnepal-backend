from django.urls import path

from careers.views import RecommendationAPIView, CareerDetailAPIView

urlpatterns = [
    #GET http://127.0.0.1:8000/api/careers/recommendations/
    path(
        "recommendations/",
        RecommendationAPIView.as_view(),
        name="recommendations",
    ),

# GET http://127.0.0.1:8000/api/careers/software-engineer/
    path(
        "<slug:slug>/",
        CareerDetailAPIView.as_view(),
        name="career-detail",
    ),


]