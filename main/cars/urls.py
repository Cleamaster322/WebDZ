from django.urls import path

from .views import *

urlpatterns = [
    path('cars/', TestAPIView.as_view()),
    path('brand/', BrandListAPIView.as_view()),
    path('brand/<int:pk>/', BrandDetailAPIView.as_view()),
]