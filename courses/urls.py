from django.urls import path

from .views import CourseDetailAPIView, CourseListAPIView


urlpatterns = [
# GET http://127.0.0.1:8000/api/courses/bachelor-of-computer-application/
    path(
        "<slug:slug>/",
        CourseDetailAPIView.as_view(),
        name="course-detail",
    ),
# GET http://127.0.0.1:8000/api/courses/
    path(
    "",
    CourseListAPIView.as_view(),
    name="course-list",
    ),

]