from django.urls import path

from .views import *

urlpatterns = [
    path('brand/', BrandListAPIView.as_view()),
    path('brand/<int:pk>/', BrandDetailAPIView.as_view()),
    path('token/', CsrfToken.as_view()),
]