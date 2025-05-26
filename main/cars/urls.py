from django.urls import path
from .views import *

urlpatterns = [
    # --- CSRF ---
    path('get_csrf_token/', get_csrf_token),

    # --- TEST ---
    path('test/', test),
    path('test1/', test1),
    path('test2/', test2),

    # --- BRANDS ---
    path('brands/', get_all_brands),
    path('brands/<int:pk>/', get_brand),
    path('brands/create/', post_brand),
    path('brands/<int:pk>/update/', update_brand),
    path('brands/<int:pk>/delete/', delete_brand),

    # --- MODELS ---
    path('models/', get_all_models),
    path('models/<int:pk>/', get_model),
    path('models/create/', post_model),
    path('models/<int:pk>/update/', update_model),
    path('models/<int:pk>/delete/', delete_model),

    # --- GENERATIONS ---
    path('generations/', get_all_generations),
    path('generations/<int:pk>/', get_generation),
    path('generations/create/', post_generation),
    path('generations/<int:pk>/update/', update_generation),
    path('generations/<int:pk>/delete/', delete_generation),

    # --- CONFIGURATIONS ---
    path('configurations/', get_all_configurations),
    path('configurations/<int:pk>/', get_configuration),
    path('configurations/create/', post_configuration),
    path('configurations/<int:pk>/update/', update_configuration),
    path('configurations/<int:pk>/delete/', delete_configuration),

    # --- CAR DATA ---
    path('car-data/', get_all_car_data),
    path('car-data/<int:pk>/', get_car_data),
    path('car-data/create/', post_car_data),
    path('car-data/<int:pk>/update/', update_car_data),
    path('car-data/<int:pk>/delete/', delete_car_data),

    # --- PROTOCOL ---
    path('protocols/', get_all_protocol),
    path('protocol/<int:pk>/', get_protocol),
    path('protocol/create/', create_protocol),

    # --- USER ---
    path('get-all-users/', get_all_users),
    path('get-user/', get_user),

    # --- WORD DOCUMENT ---
    path('create-word/', create_word),
]
