from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls')),

    path('cars/token/', TokenObtainPairView.as_view()),
    path('cars/token/refresh/', TokenRefreshView.as_view()),
    path('cars/token/verify/', TokenVerifyView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)