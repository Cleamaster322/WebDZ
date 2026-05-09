import re
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from parsers.driver import BrowserDriver
from parsers.error_writer import write_parser_error
from db.car_crud import add_car
from utils.logger import setup_logger


logger = setup_logger(__name__)


FIELD_MAPPING = {
    "Название комплектации": "configuration_name",
    "Период выпуска": "production_period",
    "Тип привода": "drive_type",
    "Тип кузова": "body_type",
    "Марка кузова": "body_mark",
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


FINAL_CAR_DATA_FIELDS = {
    "configuration_name",
    "manufacture_year",
    "drive_type",
    "body_type",
    "body_mark",
    "transmission",
    "clearance_mm",
    "seats_count",
    "vehicle_weight_kg",
    "engine_model",
    "engine_power_hp",
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
}


def clean_text(text):
    if not text:
        return ""
    return " ".join(str(text).replace("\xa0", " ").split()).strip()


def extract_int(text):
    if not text:
        return None

    match = re.search(r"-?\d+", str(text).replace(" ", ""))
    return int(match.group()) if match else None


def normalize_drive_type(value):
    value = clean_text(value).lower()

    if "перед" in value:
        return "front"
    if "зад" in value:
        return "rear"
    if "полн" in value or "4wd" in value or "awd" in value:
        return "full"

    return None


def normalize_transmission(value):
    value = clean_text(value).lower()

    if "мкпп" in value:
        return "manual"
    if "акпп" in value:
        return "automatic"
    if "вариатор" in value:
        return "variator"
    if "робот" in value:
        return "robot"
    if "редуктор" in value:
        return "reductor"

    return None


def normalize_fuel_type(value):
    value = clean_text(value).lower()

    if "бензин" in value:
        return "petrol"
    if "дизел" in value:
        return "diesel"
    if "гибрид" in value:
        return "hybrid"
    if "электр" in value:
        return "electric"

    return None


def convert_seats_to_protocol_format(seats_count):
    if seats_count is None:
        return None

    try:
        seats_count = int(seats_count)
    except (TypeError, ValueError):
        return None

    mapping = {
        2: "2",
        4: "2/2",
        5: "2/3",
        6: "2/2/2",
        7: "2/2/3",
        8: "2/3/3",
    }

    if seats_count not in mapping:
        logger.warning(f"Неизвестная конфигурация seats_count: {seats_count}")

    return mapping.get(seats_count)


def clean_tire_marking(value):
    value = clean_text(value)

    if not value:
        return None

    patterns = [
        r"\d{3}/\d{2}\s*ZR\d{2}",
        r"\d{3}/\d{2}\s*R\d{2}C",
        r"\d{3}/\d{2}\s*R\d{2}",
        r"\d{3}/\d{2}R\d{2}",
        r"\d{3}R\d{2}(?:-\w+)?",
    ]

    for pattern in patterns:
        match = re.search(pattern, value, re.IGNORECASE)
        if match:
            return clean_text(match.group())

    logger.warning(f"Не удалось точно очистить маркировку шин: {value}")
    return value[:50]


def parse_dimensions(value):
    if not value:
        return {}

    numbers = re.findall(r"\d+", str(value))

    if len(numbers) < 3:
        return {}

    return {
        "vehicle_length_mm": int(numbers[0]),
        "vehicle_width_mm": int(numbers[1]),
        "vehicle_height_mm": int(numbers[2]),
    }


def hp_to_kw(hp):
    if hp is None:
        return None

    return round(hp * 0.7355)


def kw_to_hp(kw):
    if kw is None:
        return None

    return round(kw / 0.7355)


def parse_power(value):
    """
    Основная мощность из обычной таблицы.

    Пример:
    544 (400) / 0
    """
    if not value:
        return {}

    value = clean_text(value)

    match = re.search(r"(\d+)\s*\((\d+)\)", value)
    if match:
        return {
            "engine_power_hp": int(match.group(1)),
            "engine_power_kw": int(match.group(2)),
        }

    hp_match = re.search(r"(\d+)\s*л\.?\s*с", value, re.IGNORECASE)
    if hp_match:
        hp = int(hp_match.group(1))
        return {
            "engine_power_hp": hp,
            "engine_power_kw": hp_to_kw(hp),
        }

    kw_match = re.search(r"(\d+)\s*кВт", value, re.IGNORECASE)
    if kw_match:
        kw = int(kw_match.group(1))
        return {
            "engine_power_hp": kw_to_hp(kw),
            "engine_power_kw": kw,
        }

    return {}


def parse_power_from_summary(browser):
    """
    Fallback для страниц, где в основной таблице нет строки мощности.

    Берем из верхней мини-таблицы только блок с подписью 'Мощность'.
    Это важно, потому что у мягких гибридов может быть вторая мощность
    отдельным блоком.
    """
    try:
        soup = BeautifulSoup(browser.driver.page_source, "html.parser")

        # Сначала пробуем точечно по тексту страницы.
        text = clean_text(soup.get_text(" ", strip=True))

        # Пример: "Мощность 653 л.с."
        matches = re.findall(
            r"Мощность\s+(\d+)\s*л\.?\s*с\.?",
            text,
            re.IGNORECASE,
        )

        if matches:
            hp = int(matches[0])
            return {
                "engine_power_hp": hp,
                "engine_power_kw": hp_to_kw(hp),
            }

        # На некоторых электрокарах может быть только кВт.
        kw_matches = re.findall(
            r"Мощность\s+(\d+)\s*кВт",
            text,
            re.IGNORECASE,
        )

        if kw_matches:
            kw = int(kw_matches[0])
            return {
                "engine_power_hp": kw_to_hp(kw),
                "engine_power_kw": kw,
            }

        return {}

    except Exception as e:
        logger.warning(f"Не удалось получить мощность из мини-таблицы: {e}")
        return {}


def parse_engine_type(value):
    if not value:
        return {}

    result = {}
    value = clean_text(value).lower()

    if "рядн" in value:
        result["cylinder_layout"] = "inline"
    elif "оппозит" in value:
        result["cylinder_layout"] = "opposed"
    elif "v-" in value or "v образ" in value or "v-образ" in value:
        result["cylinder_layout"] = "v_shape"

    cyl_match = re.search(r"(\d+)[-\s]*цилинд", value)
    if cyl_match:
        result["cylinders_count"] = int(cyl_match.group(1))

    return result


def parse_turbo(value):
    if not value:
        return None

    value = clean_text(value).lower()

    if value in {"—", "-", "нет"}:
        return False

    if "турбо" in value or "есть" in value:
        return True

    return None


def extract_manufacture_year_from_period(value):
    if not value:
        return None

    match = re.search(r"\b(19|20)\d{2}\b", str(value))
    return int(match.group()) if match else None


def write_car_data_error(error_type, config_id, config_name, config_link, extra=None):
    data = {
        "configuration_id": config_id,
        "configuration_name": config_name,
        "link": config_link,
    }

    if extra:
        data.update(extra)

    write_parser_error(error_type, data)


def extract_raw_data_from_page(browser, config_id=None, config_name=None, config_link=None):
    raw_data = {}

    try:
        title = clean_text(browser.driver.find_element(By.TAG_NAME, "h1").text)
        raw_data["title"] = title
    except Exception:
        pass

    try:
        table_html = browser.driver.find_element(
            By.CSS_SELECTOR,
            "div.bm-catCompTableWrap table.b-table"
        ).get_attribute("outerHTML")
    except Exception as e:
        write_car_data_error(
            "car_data_table_html_not_found",
            config_id,
            config_name,
            config_link,
            {"error": str(e)},
        )
        return raw_data

    soup = BeautifulSoup(table_html, "html.parser")

    for index, row in enumerate(soup.select("tr"), start=1):
        cols = row.select("td")

        if len(cols) != 2:
            continue

        key = clean_text(cols[0].get_text(" ", strip=True))
        value = clean_text(cols[1].get_text(" ", strip=True))

        if not key or not value:
            continue

        raw_data[key] = value

    return raw_data


def normalize_raw_data(raw_data):
    normalized = {}

    for drom_key, raw_value in raw_data.items():
        internal_key = FIELD_MAPPING.get(drom_key)

        if not internal_key:
            continue

        normalized[internal_key] = raw_value

    if "production_period" in normalized:
        normalized["manufacture_year"] = extract_manufacture_year_from_period(
            normalized["production_period"]
        )

    if "drive_type" in normalized:
        normalized["drive_type"] = normalize_drive_type(normalized["drive_type"])

    if "transmission" in normalized:
        normalized["transmission"] = normalize_transmission(normalized["transmission"])

    if "fuel_type" in normalized:
        normalized["fuel_type"] = normalize_fuel_type(normalized["fuel_type"])

    if "clearance_mm" in normalized:
        normalized["clearance_mm"] = extract_int(normalized["clearance_mm"])

    if "seats_count" in normalized:
        seats = extract_int(normalized["seats_count"])
        normalized["seats_count"] = convert_seats_to_protocol_format(seats)

    if "vehicle_weight_kg" in normalized:
        normalized["vehicle_weight_kg"] = extract_int(normalized["vehicle_weight_kg"])

    if "dimensions_mm" in normalized:
        normalized.update(parse_dimensions(normalized["dimensions_mm"]))

    if "power_raw" in normalized:
        normalized.update(parse_power(normalized["power_raw"]))

    if "engine_type_raw" in normalized:
        normalized.update(parse_engine_type(normalized["engine_type_raw"]))

    if "turbo_raw" in normalized:
        normalized["turbo_present"] = parse_turbo(normalized["turbo_raw"])

    if "front_tires" in normalized:
        normalized["front_tires"] = clean_tire_marking(normalized["front_tires"])

    if "rear_tires" in normalized:
        normalized["rear_tires"] = clean_tire_marking(normalized["rear_tires"])

    return normalized


def filter_car_data_for_protocol(normalized_data):
    return {
        key: value
        for key, value in normalized_data.items()
        if key in FINAL_CAR_DATA_FIELDS
    }


def parse_car_data_from_configuration(config, browser):
    config_id = config.get("id")
    config_name = config.get("name")
    config_link = config.get("link")

    if not config_link:
        logger.warning(
            f"Пропуск комплектации без ссылки: id={config_id}, name={config_name}"
        )

        write_car_data_error(
            "car_data_configuration_link_missing",
            config_id,
            config_name,
            config_link,
        )

        return None

    logger.info(
        f"Обработка комплектации: id={config_id}, name={config_name}, link={config_link}"
    )

    total_start = time.perf_counter()

    try:
        get_start = time.perf_counter()
        browser.get(config_link)
        get_end = time.perf_counter()

        stop_start = time.perf_counter()
        browser.driver.execute_script("window.stop();")
        stop_end = time.perf_counter()

        wait_start = time.perf_counter()
        try:
            WebDriverWait(browser.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.bm-catCompTableWrap table.b-table tr")
                )
            )
        except TimeoutException:
            wait_end = time.perf_counter()

            logger.warning(
                f"Таблица характеристик не найдена: "
                f"id={config_id}, name={config_name}, link={config_link}"
            )

            logger.info(
                f"TIMING car_data id={config_id}: "
                f"get={get_end - get_start:.3f}s, "
                f"stop={stop_end - stop_start:.3f}s, "
                f"wait={wait_end - wait_start:.3f}s, "
                f"total={wait_end - total_start:.3f}s"
            )

            write_car_data_error(
                "car_data_specs_not_found",
                config_id,
                config_name,
                config_link,
            )

            return None

        wait_end = time.perf_counter()

        raw_start = time.perf_counter()
        raw_data = extract_raw_data_from_page(
            browser,
            config_id=config_id,
            config_name=config_name,
            config_link=config_link,
        )
        raw_end = time.perf_counter()

        if not raw_data:
            logger.warning(
                f"Сырые данные car_data пустые: "
                f"id={config_id}, name={config_name}, link={config_link}"
            )

            logger.info(
                f"TIMING car_data id={config_id}: "
                f"get={get_end - get_start:.3f}s, "
                f"stop={stop_end - stop_start:.3f}s, "
                f"wait={wait_end - wait_start:.3f}s, "
                f"raw={raw_end - raw_start:.3f}s, "
                f"total={raw_end - total_start:.3f}s"
            )

            write_car_data_error(
                "car_data_raw_data_empty",
                config_id,
                config_name,
                config_link,
            )

            return None

        normalize_start = time.perf_counter()
        normalized_data = normalize_raw_data(raw_data)

        if not normalized_data.get("engine_power_hp") and not normalized_data.get("engine_power_kw"):
            summary_power = parse_power_from_summary(browser)

            if summary_power:
                normalized_data.update(summary_power)

                logger.info(
                    f"Мощность взята из мини-таблицы id={config_id}: {summary_power}"
                )

        normalize_end = time.perf_counter()

        filter_start = time.perf_counter()
        car_data = filter_car_data_for_protocol(normalized_data)
        filter_end = time.perf_counter()

        if not car_data:
            logger.warning(
                f"После фильтрации car_data пустой: "
                f"id={config_id}, name={config_name}, link={config_link}"
            )

            logger.info(
                f"TIMING car_data id={config_id}: "
                f"get={get_end - get_start:.3f}s, "
                f"stop={stop_end - stop_start:.3f}s, "
                f"wait={wait_end - wait_start:.3f}s, "
                f"raw={raw_end - raw_start:.3f}s, "
                f"normalize={normalize_end - normalize_start:.3f}s, "
                f"filter={filter_end - filter_start:.3f}s, "
                f"total={filter_end - total_start:.3f}s"
            )

            write_car_data_error(
                "car_data_filtered_data_empty",
                config_id,
                config_name,
                config_link,
                {
                    "raw_keys": list(raw_data.keys()),
                },
            )

            return None

        total_end = time.perf_counter()

        logger.info(
            f"TIMING car_data id={config_id}: "
            f"get={get_end - get_start:.3f}s, "
            f"stop={stop_end - stop_start:.3f}s, "
            f"wait={wait_end - wait_start:.3f}s, "
            f"raw={raw_end - raw_start:.3f}s, "
            f"normalize={normalize_end - normalize_start:.3f}s, "
            f"filter={filter_end - filter_start:.3f}s, "
            f"total={total_end - total_start:.3f}s"
        )

        logger.info(
            f"Собраны данные car_data для комплектации "
            f"id={config_id}, name={config_name}: {car_data}"
        )

        return car_data

    except Exception as e:
        error_end = time.perf_counter()

        logger.error(
            f"Ошибка нормализации car_data: "
            f"id={config_id}, name={config_name}, link={config_link}: {e}",
            exc_info=True,
        )

        logger.info(
            f"TIMING car_data id={config_id}: "
            f"total_before_error={error_end - total_start:.3f}s"
        )

        write_car_data_error(
            "car_data_normalize_error",
            config_id,
            config_name,
            config_link,
            {
                "error": str(e),
            },
        )

        return None


def parse_cars(configurations):
    if not configurations:
        logger.warning("В parse_cars() передан пустой список configurations")
        return []

    logger.info(
        f"Запуск парсинга car_data. Количество комплектаций: {len(configurations)}"
    )

    parsed_cars = []

    with BrowserDriver() as browser:
        for config in configurations:
            config_id = config.get("id")
            config_name = config.get("name")
            config_link = config.get("link")

            try:
                car_data = parse_car_data_from_configuration(config, browser)

                if not car_data:
                    logger.warning(
                        f"Данные car_data не собраны: "
                        f"id={config_id}, name={config_name}, link={config_link}"
                    )
                    continue

                saved = add_car(config_id, car_data)

                if not saved:
                    logger.warning(
                        f"car_data не была сохранена для комплектации "
                        f"id={config_id}, name={config_name}"
                    )

                    write_car_data_error(
                        "car_data_save_error",
                        config_id,
                        config_name,
                        config_link,
                        {
                            "car_data": car_data,
                        },
                    )

                    continue

                parsed_cars.append(
                    {
                        "configuration_id": config_id,
                        "configuration_name": config_name,
                        "car_data": car_data,
                    }
                )

                logger.info(
                    f"Данные сохранены в car_data для комплектации "
                    f"id={config_id}, name={config_name}"
                )

            except Exception as e:
                logger.error(
                    f"Ошибка при обработке комплектации "
                    f"id={config_id}, name={config_name}, link={config_link}: {e}",
                    exc_info=True,
                )

                write_car_data_error(
                    "car_data_parse_error",
                    config_id,
                    config_name,
                    config_link,
                    {
                        "error": str(e),
                    },
                )

                continue

    logger.info(
        f"Парсинг car_data завершен. Успешно обработано: "
        f"{len(parsed_cars)} из {len(configurations)}"
    )

    return parsed_cars