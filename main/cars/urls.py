from django.urls import path
from .views import *

urlpatterns = [
    # --- CSRF ---
    path('get_csrf_token/', get_csrf_token),

    # --- TEST ---
    path('test/', test),
    path('test1/', test1),
    path('test2/', test2),

    # =========================================================
    # --- BRANDS ---
    # =========================================================
    path('brands/', get_all_brands),
    path('brands/<int:pk>/', get_brand),
    path('brands/create/', post_brand),
    path('brands/<int:pk>/update/', update_brand),
    path('brands/<int:pk>/delete/', delete_brand),

    # =========================================================
    # --- MODELS ---
    # =========================================================
    path('models/', get_all_models),
    path('models/<int:pk>/', get_model),
    path('models/create/', post_model),
    path('models/<int:pk>/update/', update_model),
    path('models/<int:pk>/delete/', delete_model),

    # =========================================================
    # --- GENERATIONS ---
    # =========================================================
    path('generations/', get_all_generations),
    path('generations/<int:pk>/', get_generation),
    path('generations/create/', post_generation),
    path('generations/<int:pk>/update/', update_generation),
    path('generations/<int:pk>/delete/', delete_generation),

    # =========================================================
    # --- CONFIGURATIONS ---
    # =========================================================
    path('configurations/', get_all_configurations),
    path('configurations/<int:pk>/', get_configuration),
    path('configurations/create/', post_configuration),
    path('configurations/<int:pk>/update/', update_configuration),
    path('configurations/<int:pk>/delete/', delete_configuration),

    # =========================================================
    # --- CAR DATA ---
    # =========================================================
    path('car-data/', get_all_car_data),
    path('car-data/<int:pk>/', get_car_data),
    path('car-data/create/', post_car_data),
    path('car-data/<int:pk>/update/', update_car_data),
    path('car-data/<int:pk>/delete/', delete_car_data),

    # =========================================================
    # --- PROTOCOLS ---
    # =========================================================
    path('protocols/', get_all_protocols),
    path('protocols/create/', create_protocol),
    path('protocols/<int:pk>/', get_protocol),
    path('protocols/<int:pk>/update/', update_protocol),
    path('protocols/<int:pk>/delete/', delete_protocol),
    path('protocols/<int:protocol_id>/full/', get_full_protocol),
    path('protocols/<int:protocol_id>/generate-docx/', generate_protocol_docx_file),

    # =========================================================
    # --- MEASUREMENT ---
    # =========================================================
    path('protocols/<int:protocol_id>/measurement/', get_protocol_measurement),
    path('protocols/<int:protocol_id>/measurement/create/', create_protocol_measurement),
    path('protocols/<int:protocol_id>/measurement/update/', update_protocol_measurement),

    # =========================================================
    # --- BRAKE ---
    # =========================================================
    path('protocols/<int:protocol_id>/brake/', get_protocol_brake),
    path('protocols/<int:protocol_id>/brake/create/', create_protocol_brake),
    path('protocols/<int:protocol_id>/brake/update/', update_protocol_brake),

    # =========================================================
    # --- LIGHT ---
    # =========================================================
    path('protocols/<int:protocol_id>/light/', get_protocol_light),
    path('protocols/<int:protocol_id>/light/create/', create_protocol_light),
    path('protocols/<int:protocol_id>/light/update/', update_protocol_light),

    # =========================================================
    # --- TEST CONDITIONS ---
    # =========================================================
    path('protocols/<int:protocol_id>/test-conditions/', get_protocol_test_conditions),
    path('protocols/<int:protocol_id>/test-conditions/create/', create_protocol_test_conditions),
    path('protocols/<int:protocol_id>/test-conditions/update/', update_protocol_test_conditions),

    # =========================================================
    # --- ROAD CONDITIONS ---
    # =========================================================
    path('protocols/<int:protocol_id>/road-conditions/', get_protocol_road_conditions),
    path('protocols/<int:protocol_id>/road-conditions/create/', create_protocol_road_conditions),
    path('protocols/<int:protocol_id>/road-conditions/update/', update_protocol_road_conditions),

    # =========================================================
    # --- POWER SUPPLY ---
    # =========================================================
    path('protocols/<int:protocol_id>/power-supply/', get_protocol_power_supply),
    path('protocols/<int:protocol_id>/power-supply/create/', create_protocol_power_supply),
    path('protocols/<int:protocol_id>/power-supply/update/', update_protocol_power_supply),

    # =========================================================
    # --- PHOTOS ---
    # =========================================================
    path('protocols/<int:protocol_id>/photos/', get_protocol_photos),
    path('protocols/<int:protocol_id>/photos/create/', create_protocol_photo),
    path('protocol-photos/<int:photo_id>/update/', update_protocol_photo),
    path('protocol-photos/<int:photo_id>/delete/', delete_protocol_photo),

    # =========================================================
    # --- USERS ---
    # =========================================================
    path('get-all-users/', get_all_users),
    path('get-user/', get_user),

    # =========================================================
    # --- WORD DOCUMENTS ---
    # =========================================================
    path('create-word/', create_word),
]