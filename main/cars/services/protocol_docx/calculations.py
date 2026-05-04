from decimal import Decimal

from .formatters import decimal_value, safe_div, fmt_num


G = Decimal("9.81")


def sum_decimal(*values):
    result = Decimal("0")
    has_any = False

    for value in values:
        number = decimal_value(value)

        if number is not None:
            result += number
            has_any = True

    if not has_any:
        return None

    return result


def calc_service_brake_specific_force(brake, measurement):
    """
    Удельная тормозная сила рабочей тормозной системы.

    Сумма тормозных сил, кН / вес ТС, кН.
    Вес берём по нагрузке на оси стенда, если есть.
    """
    brake_sum_kn = sum_decimal(
        getattr(brake, "service_brake_front_left_kn", None),
        getattr(brake, "service_brake_front_right_kn", None),
        getattr(brake, "service_brake_rear_left_kn", None),
        getattr(brake, "service_brake_rear_right_kn", None),
    )

    mass_kg = sum_decimal(
        getattr(measurement, "stand_axle1_load_kg", None),
        getattr(measurement, "stand_axle2_load_kg", None),
    )

    if brake_sum_kn is None or mass_kg is None or mass_kg == 0:
        return None

    weight_kn = mass_kg * G / Decimal("1000")

    return safe_div(brake_sum_kn, weight_kn)


def calc_parking_brake_specific_force(brake, measurement):
    """
    Удельная тормозная сила стояночной тормозной системы.
    """
    brake_sum_kn = sum_decimal(
        getattr(brake, "parking_brake_left_kn", None),
        getattr(brake, "parking_brake_right_kn", None),
    )

    mass_kg = sum_decimal(
        getattr(measurement, "stand_axle1_load_kg", None),
        getattr(measurement, "stand_axle2_load_kg", None),
    )

    if brake_sum_kn is None or mass_kg is None or mass_kg == 0:
        return None

    weight_kn = mass_kg * G / Decimal("1000")

    return safe_div(brake_sum_kn, weight_kn)


def calc_total_high_beam_cd(light):
    return sum_decimal(
        getattr(light, "left_high_beam_cd", None),
        getattr(light, "right_high_beam_cd", None),
    )


def mm_to_m(value):
    number = decimal_value(value)

    if number is None:
        return None

    return number / Decimal("1000")


def build_calculated_values(protocol):
    measurement = getattr(protocol, "measurement", None)
    brake = getattr(protocol, "brake", None)
    light = getattr(protocol, "light", None)

    service_specific = calc_service_brake_specific_force(brake, measurement) if brake and measurement else None
    parking_specific = calc_parking_brake_specific_force(brake, measurement) if brake and measurement else None
    total_high_beam = calc_total_high_beam_cd(light) if light else None

    return {
        "calc_service_brake_specific_force": fmt_num(service_specific, 3),
        "calc_parking_brake_specific_force": fmt_num(parking_specific, 3),
        "calc_total_high_beam_cd": fmt_num(total_high_beam, 1),

        "vehicle_length_m": fmt_num(mm_to_m(getattr(measurement, "vehicle_length_mm", None)), 3) if measurement else "",
        "vehicle_width_m": fmt_num(mm_to_m(getattr(measurement, "vehicle_width_mm", None)), 3) if measurement else "",
        "vehicle_height_m": fmt_num(mm_to_m(getattr(measurement, "vehicle_height_mm", None)), 3) if measurement else "",
    }


def build_uncertainty_values():
    """
    Временный слой неопределённостей.

    Потом сюда аккуратно переносим формулы из Excel.
    Сейчас значения нужны, чтобы шаблон не оставался пустым.
    """
    return {
        # тормоза
        "u_service_brake_control_force_axle1_n": "5,00",
        "u_service_brake_control_force_axle2_n": "5,00",
        "u_parking_brake_control_force_n": "5,00",
        "u_service_brake_specific_force": "0,02",
        "u_parking_brake_specific_force": "0,01",
        "u_axle_1_brake_difference_pct": "4,0",
        "u_axle_2_brake_difference_pct": "4,0",
        "u_stand_axle1_load_kg": "5",
        "u_stand_axle2_load_kg": "5",

        # свет
        "u_low_beam_lower_point_mm": "0,3",
        "u_low_beam_upper_point_mm": "0,3",
        "u_fog_light_left_distance_mm": "0,3",
        "u_fog_light_right_distance_mm": "0,3",
        "u_fog_light_lower_point_mm": "0,3",
        "u_fog_light_upper_point_mm": "0,3",
        "u_brake_signal_left_distance_mm": "0,3",
        "u_brake_signal_right_distance_mm": "0,3",
        "u_brake_signal_lower_point_mm": "0,3",
        "u_brake_signal_upper_point_mm": "0,3",
        "u_additional_brake_signal_from_support_surface_mm": "0,3",
        "u_additional_brake_signal_from_glass_edge_mm": "0,3",
        "u_additional_brake_signal_optical_center_shift_mm": "0,3",
        "u_rear_fog_upper_point_mm": "0,3",
        "u_rear_fog_lower_point_mm": "0,3",
        "u_left_34v_cd": "80,0",
        "u_left_52h_cd": "80,0",
        "u_right_34v_cd": "80,0",
        "u_right_52h_cd": "80,0",
        "u_calc_total_high_beam_cd": "7320,0",
        "u_turn_signal_frequency_hz": "0,1",
        "u_turn_signal_frequency_per_min": "6",

        # шины / стекла / размеры
        "u_tire_depth_fl_mm": "0,1",
        "u_tire_depth_fr_mm": "0,1",
        "u_tire_depth_rl_mm": "0,1",
        "u_tire_depth_rr_mm": "0,1",
        "u_glass_transparency_windshield_pct": "2,0",
        "u_glass_transparency_right_pct": "2,0",
        "u_glass_transparency_left_pct": "2,0",
        "u_sun_strip_width_mm": "0,3",
        "u_bumper_to_body_distance_mm": "0,3",
        "u_protruding_elements_doors_mm": "0,3",
        "u_protruding_elements_other_mm": "0,3",
        "u_steering_backlash_deg": "0,5",
        "u_actual_speed_kmh": "0,2",
        "u_speed_by_speedometer_kmh": "0,2",
        "u_exhaust_noise_constant_db": "0,5",
        "u_exhaust_noise_deceleration_db": "0,5",
        "u_co_min_pct": "0,03",
        "u_co_max_pct": "0,03",

        # габариты
        "u_vehicle_length_m": "0,0007",
        "u_vehicle_width_m": "0,0003",
        "u_vehicle_height_m": "0,0010",
        "u_vehicle_length_mm": "0,7",
        "u_vehicle_width_mm": "0,3",
        "u_vehicle_height_mm": "1,0",
        "u_vehicle_weight_kg": "5",
        "u_axle1_load_kg": "5",
        "u_axle2_load_kg": "5",
    }