from django.urls import path

from student_profile.views import (
    StudentProfileAPIView,
    StudentProfileUpdateAPIView,
)

urlpatterns = [
    path(
        "",
        StudentProfileAPIView.as_view(),
        name="student-profile",
    ),

    path(
        "update/",
        StudentProfileUpdateAPIView.as_view(),
        name="student-profile-update",
    ),
]