"""
URL patterns for horilla_activity API
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from horilla_activity.api.views import ActivityViewSet

router = DefaultRouter()
router.register(r"activities", ActivityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
