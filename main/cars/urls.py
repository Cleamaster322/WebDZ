from django.urls import path

from .views import *

urlpatterns = [
    path('cars/', TestAPIView.as_view()),
]