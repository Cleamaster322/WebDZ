from django.urls import path

from .views import *

urlpatterns = [
    path('brand/', BrandListAPIView.as_view()),
    path('brand/<int:pk>/', BrandDetailAPIView.as_view()),
    # path('token/', CsrfToken.as_view()),
    path('test/', test),
    path('test1/', test1),
    path('test2/', test2),
    path('get_csrf_token/', get_csrf_token),

]