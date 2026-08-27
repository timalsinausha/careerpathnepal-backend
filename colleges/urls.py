from django.urls import path

from .views import CollegeDetailAPIView


urlpatterns = [
# Get http://127.0.0.1:8000/api/colleges/nepal-college-of-information-technology/
    path(
        "<slug:slug>/",
        CollegeDetailAPIView.as_view(),
        name="college-detail",
    ),

]