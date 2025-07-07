from django.urls import path
from .views import career_api

urlpatterns = [
    path('career/', career_api),  # maps to /api/career/
]