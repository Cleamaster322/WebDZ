from pathlib import Path

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .calculations import build_calculated_values, build_uncertainty_values
from .formatters import fmt_bool, fmt_date, fmt_int, fmt_num, fmt_text
from .labels import (
    CYLINDER_LAYOUT_LABELS,
    ENGINE_LAYOUT_LABELS,
    FUEL_TANK_MEASURE_LABELS,
    FUEL_TYPE_LABELS,
    HEADLIGHT_TYPE_LABELS,
    PARKING_BRAKE_LABELS,
    SERVICE_BRAKE_LABELS,
    STEERING_BOOSTER_LABELS,
    TIRE_SEASON_LABELS,
    TRANSMISSION_LABELS,
    WHEEL_FORMULA_LABELS,
    label,
)


DEFAULT_INSPECTION_PLACE = "690074, Россия, Приморский край, г. Владивосток, ул. Снеговая, д. 64"


def get_related(protocol, attr_name):
    try:
        return getattr(protocol, attr_name)
    except ObjectDoesNotExist:
        return None


def build_owner_info(protocol):
    parts = []

    if protocol.owner_name:
        parts.append(protocol.owner_name)

    if protocol.owner_address:
        parts.append(protocol.owner_address)

    if protocol.owner_phone:
        parts.append(f"тел.: {protocol.owner_phone}")

    if protocol.owner_document:
        parts.append(protocol.owner_document)

    return "\n".join(parts)


def build_manufacturer_info(protocol):
    """
    Пока в модели нет отдельных полей изготовителя.
    Если позже добавишь поля manufacturer_name / manufacturer_address,
    сюда просто подключим их.
    """
    return ""


def normalize_light_color(value):
    if not value:
        return ""

    value = str(value).strip()
    value_lower = value.lower().replace("ё", "е")

    if value_lower in ["желтый", "жёлтый"]:
        return "автожелтый"

    return value


def build_a_20_5_values(measurement):
    selected = getattr(measurement, "fuel_tank_leak_protection_measure", None)

    values = {
        "result_a_20_5_1_status": "не применяется",
        "result_a_20_5_1_conclusion": "-",
        "result_a_20_5_2_status": "не применяется",
        "result_a_20_5_2_conclusion": "-",
        "result_a_20_5_3_status": "не применяется",
        "result_a_20_5_3_conclusion": "-",
    }

    if selected == "fixed_cap":
        values["result_a_20_5_1_status"] = "соответствует"
        values["result_a_20_5_1_conclusion"] = (
            "Соответствует требованиям ТР ТС 018/2011 Приложения N 4 п.3.8.5.1"
        )

    elif selected == "structural_elements":
        values["result_a_20_5_2_status"] = "соответствует"
        values["result_a_20_5_2_conclusion"] = (
            "Соответствует требованиям ТР ТС 018/2011 Приложения N 4 п.3.8.5.2"
        )

    elif selected == "other_measure":
        values["result_a_20_5_3_status"] = "соответствует"
        values["result_a_20_5_3_conclusion"] = (
            "Соответствует требованиям ТР ТС 018/2011 Приложения N 4 п.3.8.5.3"
        )

    return values


def get_photo_path(protocol, photo_type):
    photo = protocol.photos.filter(photo_type=photo_type).order_by("sort_order", "id").first()

    if not photo or not photo.file_path:
        return ""

    raw_path = str(photo.file_path)

    if raw_path.startswith("http://") or raw_path.startswith("https://"):
        return ""

    path = Path(raw_path)

    if path.is_absolute() and path.exists():
        return str(path)

    media_path = Path(settings.MEDIA_ROOT) / raw_path

    if media_path.exists():
        return str(media_path)

    base_path = Path(settings.BASE_DIR) / raw_path

    if base_path.exists():
        return str(base_path)

    return ""


def build_photo_values(protocol):
    return {
        "photo_stand_test": get_photo_path(protocol, "stand_test_photo"),
        "photo_gas_test": get_photo_path(protocol, "gas_test_photo"),
        "photo_noise_test": get_photo_path(protocol, "noise_test_photo"),
    }

def debug_docx_context(context, protocol):
    print("\n========== DEBUG DOCX ==========")
    print(f"protocol_id: {protocol.id}")

    keys = [
        "exhaust_noise_constant_db",
        "u_exhaust_noise_constant_db",
        "exhaust_noise_deceleration_db",
        "u_exhaust_noise_deceleration_db",
    ]

    for key in keys:
        print(f"{key}: {context.get(key)}")

    print("================================\n")


def build_protocol_docx_context(protocol):
    measurement = get_related(protocol, "measurement")
    brake = get_related(protocol, "brake")
    light = get_related(protocol, "light")
    test_conditions = get_related(protocol, "test_conditions")
    road_conditions = get_related(protocol, "road_conditions")
    power_supply = get_related(protocol, "power_supply")

    context = {
        # общие
        "protocol_number": fmt_text(protocol.protocol_number),
        "protocol_date": fmt_date(protocol.protocol_date),

        # таблица 1.1
        "brand_name": fmt_text(protocol.brand_name),
        "commercial_name": fmt_text(protocol.commercial_name),
        "body_type": fmt_text(protocol.body_type),
        "vin": fmt_text(protocol.vin),
        "registration_number": fmt_text(protocol.registration_number, "отсутствует"),
        "vehicle_category": fmt_text(protocol.vehicle_category),
        "owner_info": build_owner_info(protocol),
        "owner_name": fmt_text(protocol.owner_name),
        "owner_address": fmt_text(protocol.owner_address),
        "owner_phone": fmt_text(protocol.owner_phone),
        "manufacturer_info": build_manufacturer_info(protocol),
        "inspection_place": fmt_text(protocol.inspection_place, DEFAULT_INSPECTION_PLACE),

        # условия испытаний
        "ambient_temperature_c": fmt_num(getattr(test_conditions, "ambient_temperature_c", None), 1),
        "relative_humidity_pct": fmt_num(getattr(test_conditions, "relative_humidity_pct", None), 1),
        "atmospheric_pressure_kpa": fmt_num(getattr(test_conditions, "atmospheric_pressure_kpa", None), 2),

        "road_ambient_temperature_c": fmt_num(getattr(road_conditions, "road_ambient_temperature_c", None), 1),
        "road_relative_humidity_pct": fmt_num(getattr(road_conditions, "road_relative_humidity_pct", None), 1),

        "frequency_hz": fmt_num(getattr(power_supply, "frequency_hz", None), 1),
        "phase_a_n_voltage_v": fmt_num(getattr(power_supply, "phase_a_n_voltage_v", None), 1),
        "phase_b_n_voltage_v": fmt_num(getattr(power_supply, "phase_b_n_voltage_v", None), 1),
        "phase_c_n_voltage_v": fmt_num(getattr(power_supply, "phase_c_n_voltage_v", None), 1),
        "phase_ab_voltage_v": fmt_num(getattr(power_supply, "phase_ab_voltage_v", None), 1),
        "phase_bc_voltage_v": fmt_num(getattr(power_supply, "phase_bc_voltage_v", None), 1),
        "phase_ac_voltage_v": fmt_num(getattr(power_supply, "phase_ac_voltage_v", None), 1),

        # автомобиль
        "wheel_marking_front": fmt_text(protocol.wheel_marking_front),
        "wheel_marking_rear": fmt_text(protocol.wheel_marking_rear),
        "tire_season_label": label(TIRE_SEASON_LABELS, protocol.tire_season),
        "has_spikes_label": fmt_bool(protocol.has_spikes),
        "manufacture_year": fmt_int(protocol.manufacture_year),
        "color": fmt_text(protocol.color),

        # measurement
        "wheel_formula_label": label(WHEEL_FORMULA_LABELS, getattr(measurement, "wheel_formula", None)),
        "mufflers_count": fmt_int(getattr(measurement, "mufflers_count", None)),
        "seats_count": fmt_text(getattr(measurement, "seats_count", None)),
        "steps_present_label": fmt_bool(getattr(measurement, "steps_present", None), "Наличие", "Отсутствие"),

        "engine_model": fmt_text(getattr(measurement, "engine_model", None)),
        "engine_power_kw": fmt_num(getattr(measurement, "engine_power_kw", None), 0),
        "engine_layout_label": label(ENGINE_LAYOUT_LABELS, getattr(measurement, "engine_layout", None)),
        "cylinder_layout_label": label(CYLINDER_LAYOUT_LABELS, getattr(measurement, "cylinder_layout", None)),
        "cylinders_count": fmt_int(getattr(measurement, "cylinders_count", None)),
        "fuel_type_label": label(FUEL_TYPE_LABELS, getattr(measurement, "fuel_type", None)),
        "turbo_present_label": fmt_bool(getattr(measurement, "turbo_present", None), "Наличие", "Отсутствие"),

        "steering_booster_type_label": label(
            STEERING_BOOSTER_LABELS,
            getattr(measurement, "steering_booster_type", None),
        ),
        "transmission_type_label": label(
            TRANSMISSION_LABELS,
            getattr(measurement, "transmission_type", None),
        ),

        "tire_depth_fl_mm": fmt_num(getattr(measurement, "tire_depth_fl_mm", None), 1),
        "tire_depth_fr_mm": fmt_num(getattr(measurement, "tire_depth_fr_mm", None), 1),
        "tire_depth_rl_mm": fmt_num(getattr(measurement, "tire_depth_rl_mm", None), 1),
        "tire_depth_rr_mm": fmt_num(getattr(measurement, "tire_depth_rr_mm", None), 1),

        "bumper_bends_to_body_label": fmt_bool(getattr(measurement, "bumper_bends_to_body", None)),
        "bumper_to_body_distance_mm": fmt_num(getattr(measurement, "bumper_to_body_distance_mm", None), 2),
        "opening_roof_present_label": fmt_bool(getattr(measurement, "opening_roof_present", None)),
        "fuel_tank_leak_protection_measure_label": label(
            FUEL_TANK_MEASURE_LABELS,
            getattr(measurement, "fuel_tank_leak_protection_measure", None),
        ),

        "protruding_elements_doors_mm": fmt_num(getattr(measurement, "protruding_elements_doors_mm", None), 2),
        "protruding_elements_other_mm": fmt_num(getattr(measurement, "protruding_elements_other_mm", None), 2),

        "glass_transparency_right_pct": fmt_num(getattr(measurement, "glass_transparency_right_pct", None), 1),
        "glass_transparency_left_pct": fmt_num(getattr(measurement, "glass_transparency_left_pct", None), 1),
        "glass_transparency_windshield_pct": fmt_num(
            getattr(measurement, "glass_transparency_windshield_pct", None),
            1,
        ),
        "sun_strip_width_mm": fmt_num(getattr(measurement, "sun_strip_width_mm", None), 2),

        "steering_backlash_deg": fmt_num(getattr(measurement, "steering_backlash_deg", None), 1),

        "speed_by_speedometer_kmh": fmt_num(getattr(measurement, "speed_by_speedometer_kmh", None), 1),
        "actual_speed_kmh": fmt_num(getattr(measurement, "actual_speed_kmh", None), 1),

        "exhaust_noise_constant_db": fmt_num(getattr(measurement, "exhaust_noise_constant_db", None), 1),
        "exhaust_noise_deceleration_db": fmt_num(getattr(measurement, "exhaust_noise_deceleration_db", None), 1),

        "co_min_pct": fmt_num(getattr(measurement, "co_min_pct", None), 2),
        "co_max_pct": fmt_num(getattr(measurement, "co_max_pct", None), 2),

        "light_absorption_1": fmt_num(getattr(measurement, "light_absorption_1", None), 2),
        "light_absorption_2": fmt_num(getattr(measurement, "light_absorption_2", None), 2),
        "light_absorption_3": fmt_num(getattr(measurement, "light_absorption_3", None), 2),
        "light_absorption_4": fmt_num(getattr(measurement, "light_absorption_4", None), 2),
        "light_absorption_5": fmt_num(getattr(measurement, "light_absorption_5", None), 2),
        "light_absorption_6": fmt_num(getattr(measurement, "light_absorption_6", None), 2),

        "vehicle_length_mm": fmt_num(getattr(measurement, "vehicle_length_mm", None), 1),
        "vehicle_width_mm": fmt_num(getattr(measurement, "vehicle_width_mm", None), 1),
        "vehicle_height_mm": fmt_num(getattr(measurement, "vehicle_height_mm", None), 1),
        "vehicle_weight_kg": fmt_num(getattr(measurement, "vehicle_weight_kg", None), 0),
        "axle1_load_kg": fmt_num(getattr(measurement, "axle1_load_kg", None), 0),
        "axle2_load_kg": fmt_num(getattr(measurement, "axle2_load_kg", None), 0),
        "stand_axle1_load_kg": fmt_num(getattr(measurement, "stand_axle1_load_kg", None), 0),
        "stand_axle2_load_kg": fmt_num(getattr(measurement, "stand_axle2_load_kg", None), 0),

        # brake
        "service_brake_type_label": label(SERVICE_BRAKE_LABELS, getattr(brake, "service_brake_type", None)),
        "parking_brake_type_label": label(PARKING_BRAKE_LABELS, getattr(brake, "parking_brake_type", None)),

        "service_brake_control_force_axle1_n": fmt_num(
            getattr(brake, "service_brake_control_force_axle1_n", None),
            1,
        ),
        "service_brake_control_force_axle2_n": fmt_num(
            getattr(brake, "service_brake_control_force_axle2_n", None),
            1,
        ),
        "parking_brake_control_force_n": fmt_num(getattr(brake, "parking_brake_control_force_n", None), 1),

        "axle_1_brake_difference_pct": fmt_num(getattr(brake, "axle_1_brake_difference_pct", None), 1),
        "axle_2_brake_difference_pct": fmt_num(getattr(brake, "axle_2_brake_difference_pct", None), 1),

        "service_brake_front_left_kn": fmt_num(getattr(brake, "service_brake_front_left_kn", None), 2),
        "service_brake_front_right_kn": fmt_num(getattr(brake, "service_brake_front_right_kn", None), 2),
        "service_brake_rear_left_kn": fmt_num(getattr(brake, "service_brake_rear_left_kn", None), 2),
        "service_brake_rear_right_kn": fmt_num(getattr(brake, "service_brake_rear_right_kn", None), 2),

        "parking_brake_left_kn": fmt_num(getattr(brake, "parking_brake_left_kn", None), 2),
        "parking_brake_right_kn": fmt_num(getattr(brake, "parking_brake_right_kn", None), 2),

        # light
        "low_beam_count": fmt_int(getattr(light, "low_beam_count", None)),
        "low_beam_color": normalize_light_color(getattr(light, "low_beam_color", None)),
        "high_beam_count": fmt_int(getattr(light, "high_beam_count", None)),
        "high_beam_color": normalize_light_color(getattr(light, "high_beam_color", None)),
        "front_fog_count": fmt_int(getattr(light, "front_fog_count", None)),
        "front_fog_color": normalize_light_color(getattr(light, "front_fog_color", None)),
        "reverse_light_count": fmt_int(getattr(light, "reverse_light_count", None)),
        "reverse_light_color": normalize_light_color(getattr(light, "reverse_light_color", None)),
        "turn_signal_count": fmt_int(getattr(light, "turn_signal_count", None)),
        "turn_signal_color": normalize_light_color(getattr(light, "turn_signal_color", None)),
        "front_position_light_count": fmt_int(getattr(light, "front_position_light_count", None)),
        "front_position_light_color": normalize_light_color(getattr(light, "front_position_light_color", None)),
        "rear_position_light_count": fmt_int(getattr(light, "rear_position_light_count", None)),
        "rear_position_light_color": normalize_light_color(getattr(light, "rear_position_light_color", None)),
        "main_brake_signal_count": fmt_int(getattr(light, "main_brake_signal_count", None)),
        "main_brake_signal_color": normalize_light_color(getattr(light, "main_brake_signal_color", None)),
        "additional_brake_signal_count": fmt_int(getattr(light, "additional_brake_signal_count", None)),
        "additional_brake_signal_color": normalize_light_color(getattr(light, "additional_brake_signal_color", None)),
        "rear_fog_count": fmt_int(getattr(light, "rear_fog_count", None)),
        "rear_fog_color": normalize_light_color(getattr(light, "rear_fog_color", None)),
        "plate_light_count": fmt_int(getattr(light, "plate_light_count", None)),
        "plate_light_color": normalize_light_color(getattr(light, "plate_light_color", None)),
        "daytime_running_light_count": fmt_int(getattr(light, "daytime_running_light_count", None)),
        "daytime_running_light_color": normalize_light_color(getattr(light, "daytime_running_light_color", None)),
        "parking_light_count": fmt_int(getattr(light, "parking_light_count", None)),
        "parking_light_color": normalize_light_color(getattr(light, "parking_light_color", None)),

        "headlight_type_label": label(HEADLIGHT_TYPE_LABELS, getattr(light, "headlight_type", None)),
        "headlight_washer_present_label": fmt_bool(
            getattr(light, "headlight_washer_present", None),
            "Наличие",
            "Отсутствие",
        ),

        "left_34v_cd": fmt_num(getattr(light, "left_34v_cd", None), 1),
        "left_52h_cd": fmt_num(getattr(light, "left_52h_cd", None), 1),
        "left_high_beam_cd": fmt_num(getattr(light, "left_high_beam_cd", None), 1),
        "right_34v_cd": fmt_num(getattr(light, "right_34v_cd", None), 1),
        "right_52h_cd": fmt_num(getattr(light, "right_52h_cd", None), 1),
        "right_high_beam_cd": fmt_num(getattr(light, "right_high_beam_cd", None), 1),

        "turn_signal_frequency_per_min": fmt_num(getattr(light, "turn_signal_frequency_per_min", None), 1),
        "turn_signal_frequency_hz": fmt_num(getattr(light, "turn_signal_frequency_hz", None), 1),

        "low_beam_upper_point_mm": fmt_num(getattr(light, "low_beam_upper_point_mm", None), 2),
        "low_beam_lower_point_mm": fmt_num(getattr(light, "low_beam_lower_point_mm", None), 2),

        "fog_light_upper_point_mm": fmt_num(getattr(light, "fog_light_upper_point_mm", None), 2),
        "fog_light_lower_point_mm": fmt_num(getattr(light, "fog_light_lower_point_mm", None), 2),
        "fog_light_left_distance_mm": fmt_num(getattr(light, "fog_light_left_distance_mm", None), 2),
        "fog_light_right_distance_mm": fmt_num(getattr(light, "fog_light_right_distance_mm", None), 2),

        "brake_signal_upper_point_mm": fmt_num(getattr(light, "brake_signal_upper_point_mm", None), 2),
        "brake_signal_lower_point_mm": fmt_num(getattr(light, "brake_signal_lower_point_mm", None), 2),
        "brake_signal_left_distance_mm": fmt_num(getattr(light, "brake_signal_left_distance_mm", None), 2),
        "brake_signal_right_distance_mm": fmt_num(getattr(light, "brake_signal_right_distance_mm", None), 2),

        "additional_brake_signal_from_glass_edge_mm": fmt_num(
            getattr(light, "additional_brake_signal_from_glass_edge_mm", None), 2),
        "additional_brake_signal_from_support_surface_mm": fmt_num(
            getattr(light, "additional_brake_signal_from_support_surface_mm", None), 2),
        "additional_brake_signal_optical_center_shift_mm": fmt_num(
            getattr(light, "additional_brake_signal_optical_center_shift_mm", None), 2),

        "rear_fog_upper_point_mm": fmt_num(getattr(light, "rear_fog_upper_point_mm", None), 2),
        "rear_fog_lower_point_mm": fmt_num(getattr(light, "rear_fog_lower_point_mm", None), 2),
    }

    context.update(build_a_20_5_values(measurement))
    context.update(build_calculated_values(protocol))
    context.update(build_uncertainty_values(protocol))
    context.update(build_photo_values(protocol))

    debug_docx_context(context, protocol)
    return context