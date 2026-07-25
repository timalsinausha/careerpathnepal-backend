from django.urls import path

from locations.views import (
    ProvinceListAPIView,
    DistrictListAPIView,
)

urlpatterns = [
    # http://127.0.0.1:8000/api/locations/provinces/  
    path(
        "provinces/",
        ProvinceListAPIView.as_view(),
        name="province-list",
    ),

    #  http://127.0.0.1:8000/api/locations/districts/?province=3
    path(
        "districts/",
        DistrictListAPIView.as_view(),
        name="district-list",
    ),
]