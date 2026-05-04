import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


TEST_URL = "https://www.drom.ru/catalog/toyota/sprinter/434975/"


FIELD_MAPPING = {
    "Название комплектации": "configuration_name",
    "Период выпуска": "production_period",
    "Тип привода": "drive_type",
    "Тип кузова": "body_type",
    "Тип трансмиссии": "transmission",
    "Клиренс (высота дорожного просвета), мм": "clearance_mm",
    "Число мест": "seats_count",
    "Марка двигателя": "engine_model",
    "Используемое топливо": "fuel_type",
    "Тип двигателя": "engine_type_raw",
    "Нагнетатель": "turbo_raw",
    "Максимальная мощность, л.с. (кВт) при об./мин.": "power_raw",
    "Передние колеса": "front_tires",
    "Задние колеса": "rear_tires",
    "Передние тормоза": "front_brakes",
    "Задние тормоза": "rear_brakes",
    "Габариты кузова (Д x Ш x В), мм": "dimensions_mm",
    "Масса, кг": "vehicle_weight_kg",
}


PROTOCOL_RELEVANT_FIELDS = {
    "configuration_name",
    "production_period",
    "drive_type",
    "body_type",
    "transmission",
    "clearance_mm",
    "seats_count",
    "engine_model",
    "engine_power_kw",
    "fuel_type",
    "cylinder_layout",
    "cylinders_count",
    "turbo_present",
    "front_tires",
    "rear_tires",
    "front_brakes",
    "rear_brakes",
    "vehicle_length_mm",
    "vehicle_width_mm",
    "vehicle_height_mm",
    "vehicle_weight_kg",
}


def print_block(title: str):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def clean_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\xa0", " ").split()).strip()


def to_int(value: str):
    if not value:
        return None
    match = re.search(r"-?\d+", value.replace(" ", ""))
    return int(match.group()) if match else None


def normalize_drive_type(value: str):
    value_lower = value.lower()
    if "перед" in value_lower:
        return "front"
    if "зад" in value_lower:
        return "rear"
    if "полн" in value_lower or "4wd" in value_lower or "awd" in value_lower:
        return "full"
    return value


def normalize_transmission(value: str):
    value_lower = value.lower()
    if "мкпп" in value_lower:
        return "manual"
    if "акпп" in value_lower:
        return "automatic"
    if "вариатор" in value_lower:
        return "variator"
    if "робот" in value_lower:
        return "robot"
    if "редуктор" in value_lower:
        return "reductor"
    return value


def normalize_fuel_type(value: str):
    value_lower = value.lower()
    if "бензин" in value_lower:
        return "petrol"
    if "дизел" in value_lower:
        return "diesel"
    if "гибрид" in value_lower:
        return "hybrid"
    if "электр" in value_lower:
        return "electric"
    return value


def parse_dimensions(value: str):
    if not value:
        return {}
    numbers = re.findall(r"\d+", value)
    if len(numbers) >= 3:
        return {
            "vehicle_length_mm": int(numbers[0]),
            "vehicle_width_mm": int(numbers[1]),
            "vehicle_height_mm": int(numbers[2]),
        }
    return {}


def parse_power(value: str):
    """
    73 (54) / 6000 -> engine_power_hp, engine_power_kw, engine_power_rpm
    Но в итог для протокола оставляем только engine_power_kw
    """
    if not value:
        return {}

    match = re.search(r"(\d+)\s*\((\d+)\)\s*/\s*(\d+)", value)
    if match:
        return {
            "engine_power_hp": int(match.group(1)),
            "engine_power_kw": int(match.group(2)),
            "engine_power_rpm": int(match.group(3)),
        }

    return {}


def parse_engine_type(value: str):
    """
    Рядный, 4-цилиндровый -> cylinder_layout, cylinders_count
    """
    if not value:
        return {}

    result = {}
    value_lower = value.lower()

    if "рядн" in value_lower:
        result["cylinder_layout"] = "inline"
    elif "оппозит" in value_lower:
        result["cylinder_layout"] = "opposed"
    elif "v-" in value_lower or "v образ" in value_lower or "v-образ" in value_lower:
        result["cylinder_layout"] = "v_shape"

    cyl_match = re.search(r"(\d+)[-\s]*цилинд", value_lower)
    if cyl_match:
        result["cylinders_count"] = int(cyl_match.group(1))

    return result


def parse_turbo(value: str):
    if not value:
        return None

    value_lower = value.lower()

    if value_lower in {"—", "-", "нет"}:
        return False

    if "турбо" in value_lower or "есть" in value_lower:
        return True

    return None


def extract_manufacture_year_from_period(value: str):
    """
    1991 - декабрь 1993 -> 1991
    2026 -> 2026
    """
    if not value:
        return None

    match = re.search(r"\b(19|20)\d{2}\b", value)
    if match:
        return int(match.group())

    return None


def normalize_raw_data(raw_data: dict) -> dict:
    normalized = {}

    for drom_key, raw_value in raw_data.items():
        internal_key = FIELD_MAPPING.get(drom_key)
        if not internal_key:
            continue
        normalized[internal_key] = raw_value

    # Простые преобразования
    if "clearance_mm" in normalized:
        normalized["clearance_mm"] = to_int(normalized["clearance_mm"])

    if "seats_count" in normalized:
        normalized["seats_count"] = to_int(normalized["seats_count"])

    if "vehicle_weight_kg" in normalized:
        normalized["vehicle_weight_kg"] = to_int(normalized["vehicle_weight_kg"])

    if "drive_type" in normalized:
        normalized["drive_type"] = normalize_drive_type(normalized["drive_type"])

    if "transmission" in normalized:
        normalized["transmission"] = normalize_transmission(normalized["transmission"])

    if "fuel_type" in normalized:
        normalized["fuel_type"] = normalize_fuel_type(normalized["fuel_type"])

    # Производный год выпуска
    if "production_period" in normalized:
        normalized["manufacture_year"] = extract_manufacture_year_from_period(
            normalized["production_period"]
        )

    # Размеры
    if "dimensions_mm" in normalized:
        normalized.update(parse_dimensions(normalized["dimensions_mm"]))

    # Мощность
    if "power_raw" in normalized:
        normalized.update(parse_power(normalized["power_raw"]))

    # Тип двигателя
    if "engine_type_raw" in normalized:
        normalized.update(parse_engine_type(normalized["engine_type_raw"]))

    # Турбина
    if "turbo_raw" in normalized:
        normalized["turbo_present"] = parse_turbo(normalized["turbo_raw"])

    return normalized


def filter_protocol_fields(normalized_data: dict) -> dict:
    filtered = {}

    for key, value in normalized_data.items():
        if key in PROTOCOL_RELEVANT_FIELDS:
            filtered[key] = value

    # manufacture_year полезен для формы, хотя он производный
    if "manufacture_year" in normalized_data:
        filtered["manufacture_year"] = normalized_data["manufacture_year"]

    return filtered


class CarDataParserTest:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse_raw_data(self, url: str) -> dict:
        self.driver.get(url)
        time.sleep(3)

        raw_data = {}

        try:
            title = clean_text(self.driver.find_element(By.TAG_NAME, "h1").text)
            raw_data["title"] = title
        except Exception as e:
            print(f"Ошибка получения title: {e}")

        try:
            rows = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.bm-catCompTableWrap table.b-table tr"
            )

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")

                if len(cols) != 2:
                    continue

                key = clean_text(cols[0].text)
                value = clean_text(cols[1].text)

                if not key or not value:
                    continue

                raw_data[key] = value

        except Exception as e:
            print(f"Ошибка парсинга таблицы: {e}")

        return raw_data

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    parser = CarDataParserTest()

    try:
        raw_data = parser.parse_raw_data(TEST_URL)
        normalized_data = normalize_raw_data(raw_data)
        filtered_data = filter_protocol_fields(normalized_data)

        print_block("RAW DATA")
        for key, value in raw_data.items():
            print(f"{key}: {value}")

        print_block("FILTERED DATA FOR PROTOCOL")
        for key, value in filtered_data.items():
            print(f"{key}: {value}")

    finally:
        parser.close()