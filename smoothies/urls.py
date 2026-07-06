from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SmoothieAPIView, SmoothieViewSet

router = DefaultRouter()
router.register(r"smoothies", SmoothieViewSet, basename="smoothie")

urlpatterns = [
    path("get/", SmoothieAPIView.as_view(), name="smoothie-stats"),
    path("", include(router.urls)),
]