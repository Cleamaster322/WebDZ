from pathlib import Path

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .calculations import (
    build_calculated_values,
    build_uncertainty_values,
    calc_light_absorption_average,
)
from .formatters import decimal_value, fmt_bool, fmt_date, fmt_int, fmt_num, fmt_text
from .labels import (
    CYLINDER_LAYOUT_LABELS,
    ENGINE_LAYOUT_LABELS,
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


# =========================
# Базовые helpers
# =========================

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


def is_positive_count(value):
    number = decimal_value(value)

    if number is None:
        return False

    return number > 0


def is_true(value):
    return value is True


def is_fuel_petrol_like(value):
    return value in ["petrol", "hybrid"]


def is_fuel_diesel(value):
    return value == "diesel"


def conclusion_text(*lines):
    return "\n".join(lines)


# =========================
# Динамические результаты:
# статус + заключение
# =========================

def make_result(is_applicable, conclusion):
    """
    Общее правило для подсказок вида:
    "Соответствует/не применяется".

    Если элемент/условие есть:
        статус = соответствует
        заключение = полный текст требований

    Если элемента/условия нет:
        статус = не применяется
        заключение = "-"
    """
    if is_applicable:
        return "соответствует", conclusion

    return "не применяется", "-"


def add_result_pair(context, key_prefix, is_applicable, conclusion):
    status, conclusion_value = make_result(is_applicable, conclusion)

    context[f"{key_prefix}_status"] = status
    context[f"{key_prefix}_conclusion"] = conclusion_value


def add_direct_result_pair(context, key_prefix, status, conclusion):
    """
    Для случаев, где в статусной ячейке должен быть не просто текст
    "соответствует", а конкретное значение:
    - среднее значение дымности;
    - пробег более/менее 3000 км.
    """
    context[f"{key_prefix}_status"] = status

    if status in ["не применяется", "не указано"]:
        context[f"{key_prefix}_conclusion"] = "-"
    else:
        context[f"{key_prefix}_conclusion"] = conclusion


CONCLUSIONS = {
    "a_3_2": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложение № 3 п. 16.1;",
        "Приложение №4 п.5.1",
    ),

    "a_6_5": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения №4 п.1.1.5",
    ),

    "a_8_7": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 4 п.1.3.7",
    ),

    "a_8_10_3": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 4 п.1.3.10.3",
    ),

    "a_8_13_1": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 4 п.1.3.13.1",
    ),

    "a_8_20_3": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.8.3",
    ),

    "a_8_20_8": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.8.8",
    ),

    "a_8_24_1": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.12.1",
    ),

    "a_8_24_2": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.12.2",
    ),

    "a_8_24_3": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.12.3",
    ),

    "a_8_25": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.13",
    ),

    "a_8_27": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.3.15",
    ),

    "a_10_5": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.5.5",
    ),

    "a_10_6": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.5.4",
    ),

    "a_16_17": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 4 п.3.6.17",
    ),

    "a_18_5": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 4 п.3.4.4.5",
    ),

    "a_21_7": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения №8 п.9.1",
    ),

    "a_21_8": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения №8 п.9.2",
    ),

    "a_21_9": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения №8 п.9.3",
    ),

    "a_22_5_1": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.1",
    ),

    "a_22_5_2": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.2",
    ),

    "a_22_5_3": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.3",
    ),

    "a_22_5_4": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.4",
    ),

    "a_22_5_5": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.5",
    ),

    "a_22_5_6_1": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.6.1",
    ),

    "a_22_5_6_2": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.6.2",
    ),

    "a_22_5_6_3": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.9.8.6.3",
    ),

    "a_26_12": conclusion_text(
        "Соответствует требованиям",
        "ТР ТС 018/2011",
        "Приложения N 8 п.10.12",
    ),
}


def build_dynamic_result_values(protocol, measurement, light):
    values = {}

    fuel_type = getattr(measurement, "fuel_type", None)
    tire_season = getattr(protocol, "tire_season", None)
    has_spikes = getattr(protocol, "has_spikes", None)

    front_fog_present = is_positive_count(getattr(light, "front_fog_count", None))
    rear_fog_present = is_positive_count(getattr(light, "rear_fog_count", None))
    daytime_running_present = is_positive_count(
        getattr(light, "daytime_running_light_count", None)
    )

    parking_light_present = (
        is_positive_count(getattr(light, "parking_light_count", None))
        or is_positive_count(getattr(light, "rear_parking_light_count", None))
    )

    adaptive_front_lighting_present = is_positive_count(
        getattr(light, "adaptive_front_lighting_count", None)
    )

    washer_present = is_true(getattr(light, "headlight_washer_present", None))

    # А.3.2 — отдельного поля пока нет, поэтому по умолчанию соответствует.
    add_result_pair(
        values,
        "result_a_3_2",
        True,
        CONCLUSIONS["a_3_2"],
    )

    # А.6.5 — блокировка рулевого управления
    add_result_pair(
        values,
        "result_a_6_5",
        is_true(getattr(measurement, "steering_lock_present", None)),
        CONCLUSIONS["a_6_5"],
    )

    # А.8.7 — корректировка/система переднего освещения.
    # Если адаптивная система есть или омыватели есть — соответствует.
    # Если ничего из этого нет — не применяется.
    add_result_pair(
        values,
        "result_a_8_7",
        adaptive_front_lighting_present or washer_present,
        CONCLUSIONS["a_8_7"],
    )

    # А.8.10.3 — передние ПТФ
    add_result_pair(
        values,
        "result_a_8_10_3",
        front_fog_present,
        CONCLUSIONS["a_8_10_3"],
    )

    # А.8.13.1 — задние ПТФ
    add_result_pair(
        values,
        "result_a_8_13_1",
        rear_fog_present,
        CONCLUSIONS["a_8_13_1"],
    )

    # А.8.20.3 — омыватели фар
    add_result_pair(
        values,
        "result_a_8_20_3",
        washer_present,
        CONCLUSIONS["a_8_20_3"],
    )

    # А.8.20.8 — передние ПТФ
    add_result_pair(
        values,
        "result_a_8_20_8",
        front_fog_present,
        CONCLUSIONS["a_8_20_8"],
    )

    # А.8.24.1–А.8.24.3 — задние ПТФ
    add_result_pair(
        values,
        "result_a_8_24_1",
        rear_fog_present,
        CONCLUSIONS["a_8_24_1"],
    )
    add_result_pair(
        values,
        "result_a_8_24_2",
        rear_fog_present,
        CONCLUSIONS["a_8_24_2"],
    )
    add_result_pair(
        values,
        "result_a_8_24_3",
        rear_fog_present,
        CONCLUSIONS["a_8_24_3"],
    )

    # А.8.25 — стояночные огни
    add_result_pair(
        values,
        "result_a_8_25",
        parking_light_present,
        CONCLUSIONS["a_8_25"],
    )

    # А.8.27 — дневные ходовые огни
    add_result_pair(
        values,
        "result_a_8_27",
        daytime_running_present,
        CONCLUSIONS["a_8_27"],
    )

    # А.10.5 — зимние шины
    add_result_pair(
        values,
        "result_a_10_5",
        tire_season == "winter",
        CONCLUSIONS["a_10_5"],
    )

    # А.10.6 — шипы
    add_result_pair(
        values,
        "result_a_10_6",
        tire_season == "winter" and has_spikes is True,
        CONCLUSIONS["a_10_6"],
    )

    # А.16.17 — подножки
    add_result_pair(
        values,
        "result_a_16_17",
        is_true(getattr(measurement, "steps_present", None)),
        CONCLUSIONS["a_16_17"],
    )

    # А.18.5 — открывающаяся крыша
    add_result_pair(
        values,
        "result_a_18_5",
        is_true(getattr(measurement, "opening_roof_present", None)),
        CONCLUSIONS["a_18_5"],
    )

    # А.21.7 — CO, применяется для бензина/гибрида.
    add_result_pair(
        values,
        "result_a_21_7",
        is_fuel_petrol_like(fuel_type),
        CONCLUSIONS["a_21_7"],
    )

    # А.21.8 — дымность, применяется для дизеля.
    # В статусной ячейке выводим среднее значение коэффициента поглощения.
    if is_fuel_diesel(fuel_type):
        average = calc_light_absorption_average(measurement)

        if average is not None:
            status = f"{fmt_num(average, 3)} м-1"
        else:
            status = "соответствует"

        add_direct_result_pair(
            values,
            "result_a_21_8",
            status,
            CONCLUSIONS["a_21_8"],
        )
    else:
        add_direct_result_pair(
            values,
            "result_a_21_8",
            "не применяется",
            "-",
        )

    # А.21.9 — пробег более/менее 3000 км.
    mileage = decimal_value(getattr(measurement, "mileage_km", None))

    if mileage is None:
        add_direct_result_pair(
            values,
            "result_a_21_9",
            "не указано",
            "-",
        )
    elif mileage >= 3000:
        add_direct_result_pair(
            values,
            "result_a_21_9",
            f"более 3000 км. Пробег: {fmt_num(mileage, 0)} км",
            CONCLUSIONS["a_21_9"],
        )
    else:
        add_direct_result_pair(
            values,
            "result_a_21_9",
            f"менее 3000 км. Пробег: {fmt_num(mileage, 0)} км",
            "-",
        )

    # А.22.5.* — газобаллонное оборудование.
    # Если ГБО есть — соответствует.
    # Если ГБО нет — не применяется и заключение "-".
    gas_equipment_present = is_true(
        getattr(measurement, "gas_equipment_present", None)
    )

    for suffix in [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6_1",
        "6_2",
        "6_3",
    ]:
        conclusion_key = f"a_22_5_{suffix}"
        result_key = f"result_a_22_5_{suffix}"

        add_result_pair(
            values,
            result_key,
            gas_equipment_present,
            CONCLUSIONS[conclusion_key],
        )

    # А.26.12 — запасное колесо
    add_result_pair(
        values,
        "result_a_26_12",
        is_true(getattr(measurement, "spare_wheel_present", None)),
        CONCLUSIONS["a_26_12"],
    )

    return values


# =========================
# Фото
# =========================

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
        "result_a_8_10_3_status",
        "result_a_8_10_3_conclusion",
        "result_a_21_9_status",
        "result_a_21_9_conclusion",
    ]

    for key in keys:
        print(f"{key}: {context.get(key)}")

    print("================================\n")


# =========================
# Главная сборка context для DOCX
# =========================

def build_protocol_docx_context(protocol):
    measurement = get_related(protocol, "measurement")
    brake = get_related(protocol, "brake")
    light = get_related(protocol, "light")
    test_conditions = get_related(protocol, "test_conditions")
    road_conditions = get_related(protocol, "road_conditions")
    power_supply = get_related(protocol, "power_supply")

    context = {
        # =========================
        # Общие данные
        # =========================
        "protocol_number": fmt_text(protocol.protocol_number),
        "protocol_date": fmt_date(protocol.protocol_date),

        # =========================
        # Таблица 1.1
        # =========================
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

        # =========================
        # Условия испытаний
        # =========================
        "ambient_temperature_c": fmt_num(
            getattr(test_conditions, "ambient_temperature_c", None),
            1,
        ),
        "relative_humidity_pct": fmt_num(
            getattr(test_conditions, "relative_humidity_pct", None),
            1,
        ),
        "atmospheric_pressure_kpa": fmt_num(
            getattr(test_conditions, "atmospheric_pressure_kpa", None),
            2,
        ),

        "road_ambient_temperature_c": fmt_num(
            getattr(road_conditions, "road_ambient_temperature_c", None),
            1,
        ),
        "road_relative_humidity_pct": fmt_num(
            getattr(road_conditions, "road_relative_humidity_pct", None),
            1,
        ),

        "frequency_hz": fmt_num(getattr(power_supply, "frequency_hz", None), 1),
        "phase_a_n_voltage_v": fmt_num(getattr(power_supply, "phase_a_n_voltage_v", None), 1),
        "phase_b_n_voltage_v": fmt_num(getattr(power_supply, "phase_b_n_voltage_v", None), 1),
        "phase_c_n_voltage_v": fmt_num(getattr(power_supply, "phase_c_n_voltage_v", None), 1),
        "phase_ab_voltage_v": fmt_num(getattr(power_supply, "phase_ab_voltage_v", None), 1),
        "phase_bc_voltage_v": fmt_num(getattr(power_supply, "phase_bc_voltage_v", None), 1),
        "phase_ac_voltage_v": fmt_num(getattr(power_supply, "phase_ac_voltage_v", None), 1),

        # =========================
        # Автомобиль
        # =========================
        "wheel_marking_front": fmt_text(protocol.wheel_marking_front),
        "wheel_marking_rear": fmt_text(protocol.wheel_marking_rear),
        "tire_season_label": label(TIRE_SEASON_LABELS, protocol.tire_season),
        "has_spikes_label": fmt_bool(protocol.has_spikes),
        "manufacture_year": fmt_int(protocol.manufacture_year),
        "color": fmt_text(protocol.color),

        # =========================
        # Measurement
        # =========================
        "wheel_formula_label": label(
            WHEEL_FORMULA_LABELS,
            getattr(measurement, "wheel_formula", None),
        ),
        "mufflers_count": fmt_int(getattr(measurement, "mufflers_count", None)),
        "seats_count": fmt_text(getattr(measurement, "seats_count", None)),
        "steps_present_label": fmt_bool(
            getattr(measurement, "steps_present", None),
            "Наличие",
            "Отсутствие",
        ),

        "engine_model": fmt_text(getattr(measurement, "engine_model", None)),
        "engine_power_kw": fmt_num(getattr(measurement, "engine_power_kw", None), 0),
        "engine_layout_label": label(
            ENGINE_LAYOUT_LABELS,
            getattr(measurement, "engine_layout", None),
        ),
        "cylinder_layout_label": label(
            CYLINDER_LAYOUT_LABELS,
            getattr(measurement, "cylinder_layout", None),
        ),
        "cylinders_count": fmt_int(getattr(measurement, "cylinders_count", None)),
        "fuel_type_label": label(
            FUEL_TYPE_LABELS,
            getattr(measurement, "fuel_type", None),
        ),
        "turbo_present_label": fmt_bool(
            getattr(measurement, "turbo_present", None),
            "Наличие",
            "Отсутствие",
        ),

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

        "bumper_bends_to_body_label": fmt_bool(
            getattr(measurement, "bumper_bends_to_body", None)
        ),
        "bumper_to_body_distance_mm": fmt_num(
            getattr(measurement, "bumper_to_body_distance_mm", None),
            2,
        ),
        "opening_roof_present_label": fmt_bool(
            getattr(measurement, "opening_roof_present", None)
        ),

        "protruding_elements_doors_mm": fmt_num(
            getattr(measurement, "protruding_elements_doors_mm", None),
            2,
        ),
        "protruding_elements_other_mm": fmt_num(
            getattr(measurement, "protruding_elements_other_mm", None),
            2,
        ),

        "glass_transparency_right_pct": fmt_num(
            getattr(measurement, "glass_transparency_right_pct", None),
            1,
        ),
        "glass_transparency_left_pct": fmt_num(
            getattr(measurement, "glass_transparency_left_pct", None),
            1,
        ),
        "glass_transparency_windshield_pct": fmt_num(
            getattr(measurement, "glass_transparency_windshield_pct", None),
            1,
        ),
        "sun_strip_width_mm": fmt_num(
            getattr(measurement, "sun_strip_width_mm", None),
            2,
        ),

        "steering_backlash_deg": fmt_num(
            getattr(measurement, "steering_backlash_deg", None),
            1,
        ),

        "speed_by_speedometer_kmh": fmt_num(
            getattr(measurement, "speed_by_speedometer_kmh", None),
            1,
        ),
        "actual_speed_kmh": fmt_num(
            getattr(measurement, "actual_speed_kmh", None),
            1,
        ),

        "exhaust_noise_constant_db": fmt_num(
            getattr(measurement, "exhaust_noise_constant_db", None),
            1,
        ),
        "exhaust_noise_deceleration_db": fmt_num(
            getattr(measurement, "exhaust_noise_deceleration_db", None),
            1,
        ),

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

        "mileage_km": fmt_num(getattr(measurement, "mileage_km", None), 0),
        "spare_wheel_present_label": fmt_bool(
            getattr(measurement, "spare_wheel_present", None),
            "Наличие",
            "Отсутствие",
        ),
        "steering_lock_present_label": fmt_bool(
            getattr(measurement, "steering_lock_present", None),
            "Наличие",
            "Отсутствие",
        ),
        "gas_equipment_present_label": fmt_bool(
            getattr(measurement, "gas_equipment_present", None),
            "Наличие",
            "Отсутствие",
        ),

        # =========================
        # Brake
        # =========================
        "service_brake_type_label": label(
            SERVICE_BRAKE_LABELS,
            getattr(brake, "service_brake_type", None),
        ),
        "parking_brake_type_label": label(
            PARKING_BRAKE_LABELS,
            getattr(brake, "parking_brake_type", None),
        ),

        "service_brake_control_force_axle1_n": fmt_num(
            getattr(brake, "service_brake_control_force_axle1_n", None),
            1,
        ),
        "service_brake_control_force_axle2_n": fmt_num(
            getattr(brake, "service_brake_control_force_axle2_n", None),
            1,
        ),
        "parking_brake_control_force_n": fmt_num(
            getattr(brake, "parking_brake_control_force_n", None),
            1,
        ),

        "axle_1_brake_difference_pct": fmt_num(
            getattr(brake, "axle_1_brake_difference_pct", None),
            1,
        ),
        "axle_2_brake_difference_pct": fmt_num(
            getattr(brake, "axle_2_brake_difference_pct", None),
            1,
        ),

        "service_brake_front_left_kn": fmt_num(
            getattr(brake, "service_brake_front_left_kn", None),
            2,
        ),
        "service_brake_front_right_kn": fmt_num(
            getattr(brake, "service_brake_front_right_kn", None),
            2,
        ),
        "service_brake_rear_left_kn": fmt_num(
            getattr(brake, "service_brake_rear_left_kn", None),
            2,
        ),
        "service_brake_rear_right_kn": fmt_num(
            getattr(brake, "service_brake_rear_right_kn", None),
            2,
        ),

        "parking_brake_left_kn": fmt_num(getattr(brake, "parking_brake_left_kn", None), 2),
        "parking_brake_right_kn": fmt_num(getattr(brake, "parking_brake_right_kn", None), 2),

        # =========================
        # Light
        # =========================
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

        "front_position_light_count": fmt_int(
            getattr(light, "front_position_light_count", None)
        ),
        "front_position_light_color": normalize_light_color(
            getattr(light, "front_position_light_color", None)
        ),

        "rear_position_light_count": fmt_int(
            getattr(light, "rear_position_light_count", None)
        ),
        "rear_position_light_color": normalize_light_color(
            getattr(light, "rear_position_light_color", None)
        ),

        "main_brake_signal_count": fmt_int(
            getattr(light, "main_brake_signal_count", None)
        ),
        "main_brake_signal_color": normalize_light_color(
            getattr(light, "main_brake_signal_color", None)
        ),

        "additional_brake_signal_count": fmt_int(
            getattr(light, "additional_brake_signal_count", None)
        ),
        "additional_brake_signal_color": normalize_light_color(
            getattr(light, "additional_brake_signal_color", None)
        ),

        "rear_fog_count": fmt_int(getattr(light, "rear_fog_count", None)),
        "rear_fog_color": normalize_light_color(getattr(light, "rear_fog_color", None)),

        "plate_light_count": fmt_int(getattr(light, "plate_light_count", None)),
        "plate_light_color": normalize_light_color(getattr(light, "plate_light_color", None)),

        "daytime_running_light_count": fmt_int(
            getattr(light, "daytime_running_light_count", None)
        ),
        "daytime_running_light_color": normalize_light_color(
            getattr(light, "daytime_running_light_color", None)
        ),

        "parking_light_count": fmt_int(getattr(light, "parking_light_count", None)),
        "parking_light_color": normalize_light_color(
            getattr(light, "parking_light_color", None)
        ),

        "rear_parking_light_count": fmt_int(
            getattr(light, "rear_parking_light_count", None)
        ),
        "rear_parking_light_color": normalize_light_color(
            getattr(light, "rear_parking_light_color", None)
        ),

        "adaptive_front_lighting_count": fmt_int(
            getattr(light, "adaptive_front_lighting_count", None)
        ),
        "adaptive_front_lighting_color": normalize_light_color(
            getattr(light, "adaptive_front_lighting_color", None)
        ),

        "headlight_type_label": label(
            HEADLIGHT_TYPE_LABELS,
            getattr(light, "headlight_type", None),
        ),
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

        "turn_signal_frequency_per_min": fmt_num(
            getattr(light, "turn_signal_frequency_per_min", None),
            1,
        ),
        "turn_signal_frequency_hz": fmt_num(
            getattr(light, "turn_signal_frequency_hz", None),
            1,
        ),

        "low_beam_upper_point_mm": fmt_num(
            getattr(light, "low_beam_upper_point_mm", None),
            2,
        ),
        "low_beam_lower_point_mm": fmt_num(
            getattr(light, "low_beam_lower_point_mm", None),
            2,
        ),

        "fog_light_upper_point_mm": fmt_num(
            getattr(light, "fog_light_upper_point_mm", None),
            2,
        ),
        "fog_light_lower_point_mm": fmt_num(
            getattr(light, "fog_light_lower_point_mm", None),
            2,
        ),
        "fog_light_left_distance_mm": fmt_num(
            getattr(light, "fog_light_left_distance_mm", None),
            2,
        ),
        "fog_light_right_distance_mm": fmt_num(
            getattr(light, "fog_light_right_distance_mm", None),
            2,
        ),

        "brake_signal_upper_point_mm": fmt_num(
            getattr(light, "brake_signal_upper_point_mm", None),
            2,
        ),
        "brake_signal_lower_point_mm": fmt_num(
            getattr(light, "brake_signal_lower_point_mm", None),
            2,
        ),
        "brake_signal_left_distance_mm": fmt_num(
            getattr(light, "brake_signal_left_distance_mm", None),
            2,
        ),
        "brake_signal_right_distance_mm": fmt_num(
            getattr(light, "brake_signal_right_distance_mm", None),
            2,
        ),

        "additional_brake_signal_from_glass_edge_mm": fmt_num(
            getattr(light, "additional_brake_signal_from_glass_edge_mm", None),
            2,
        ),
        "additional_brake_signal_from_support_surface_mm": fmt_num(
            getattr(light, "additional_brake_signal_from_support_surface_mm", None),
            2,
        ),
        "additional_brake_signal_optical_center_shift_mm": fmt_num(
            getattr(light, "additional_brake_signal_optical_center_shift_mm", None),
            2,
        ),

        "rear_fog_upper_point_mm": fmt_num(
            getattr(light, "rear_fog_upper_point_mm", None),
            2,
        ),
        "rear_fog_lower_point_mm": fmt_num(
            getattr(light, "rear_fog_lower_point_mm", None),
            2,
        ),
    }

    context.update(build_dynamic_result_values(protocol, measurement, light))
    context.update(build_calculated_values(protocol))
    context.update(build_uncertainty_values(protocol))
    context.update(build_photo_values(protocol))

    debug_docx_context(context, protocol)

    return context