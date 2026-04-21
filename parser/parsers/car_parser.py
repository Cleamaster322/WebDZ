import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from parsers.driver import BrowserDriver
from db.car_crud import add_car
from utils.logger import setup_logger


logger = setup_logger(__name__)


def extract_int(text):
    """Извлекает первое целое число из строки."""
    if not text:
        return None

    numbers = re.findall(r"\d+", str(text).replace(" ", ""))
    return int(numbers[0]) if numbers else None


def extract_float(text):
    """Извлекает первое число с плавающей точкой из строки."""
    if not text:
        return None

    numbers = re.findall(r"\d+[.,]?\d*", str(text).replace(" ", ""))
    return float(numbers[0].replace(",", ".")) if numbers else None


def extract_power_values(power_text):
    """
    Извлекает мощность в л.с. и кВт из строки вида:
    '123 л.с. (90 кВт)' или похожих вариантов.
    """
    if not power_text:
        return None, None

    hp_match = re.search(r"(\d+[.,]?\d*)\s*л\.?с\.?", power_text, re.IGNORECASE)
    kw_match = re.search(r"(\d+[.,]?\d*)\s*кВт", power_text, re.IGNORECASE)

    hp = int(float(hp_match.group(1).replace(",", "."))) if hp_match else None
    kw = int(float(kw_match.group(1).replace(",", "."))) if kw_match else None

    return hp, kw


def get_engine_capacity(raw_data):
    """Определяет значение объема/емкости двигателя."""
    if "Объем" in raw_data:
        return extract_float(raw_data["Объем"])
    if "Ёмкость" in raw_data:
        return extract_float(raw_data["Ёмкость"])
    return None


def parse_cars(configurations):
    """
    Парсит характеристики автомобилей по списку комплектаций
    и сохраняет результат в таблицу car_data.
    """
    if not configurations:
        logger.warning("В parse_cars() передан пустой список configurations")
        return []

    logger.info(f"Запуск парсинга автомобилей. Количество комплектаций: {len(configurations)}")

    parsed_cars = []

    with BrowserDriver() as browser:
        for config in configurations:
            config_id = config.get("id")
            config_name = config.get("name")
            config_link = config.get("link")

            try:
                if not config_link:
                    logger.warning(
                        f"Пропуск комплектации без ссылки: id={config_id}, name={config_name}"
                    )
                    continue

                logger.info(
                    f"Обработка комплектации: id={config_id}, name={config_name}, link={config_link}"
                )

                browser.get(config_link)

                try:
                    specs_block = WebDriverWait(browser.driver, 3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "b-model-specs"))
                    )
                except TimeoutException:
                    logger.warning(
                        f"Блок характеристик b-model-specs не найден: "
                        f"id={config_id}, name={config_name}, link={config_link}"
                    )
                    continue

                groups = specs_block.find_elements(By.CLASS_NAME, "bm-modelSpecsGroup")

                raw_data = {}
                for group in groups:
                    try:
                        label = group.find_element(
                            By.CLASS_NAME, "b-model-specs__label"
                        ).text.strip()
                        value = group.find_element(
                            By.CLASS_NAME, "b-model-specs__text"
                        ).text.strip()

                        if label:
                            raw_data[label] = value

                    except Exception as e:
                        logger.warning(
                            f"Ошибка при парсинге группы характеристик "
                            f"для комплектации id={config_id}, name={config_name}: {e}"
                        )
                        continue

                engine_power_hp, engine_power_kw = extract_power_values(
                    raw_data.get("Мощность", "")
                )
                engine_capacity = get_engine_capacity(raw_data)

                car_data = {
                    "front_tires": raw_data.get("Передние шины"),
                    "rear_tires": raw_data.get("Задние шины"),
                    "engine_capacity": engine_capacity,
                    "engine_power_hp": engine_power_hp,
                    "engine_power_kw": engine_power_kw,
                    "consumption": extract_float(raw_data.get("Расход", "")),
                    "fuel_type": raw_data.get("Тип топлива"),
                    "transmission": raw_data.get("Трансмиссия"),
                    "drive_type": raw_data.get("Привод"),
                    "seats": extract_int(raw_data.get("Кол-во мест", "")),
                    "doors": extract_int(raw_data.get("Кол-во дверей", "")),
                    "clearance": extract_int(raw_data.get("Клиренс", "")),
                    "trunk_volume": extract_int(raw_data.get("Объем багажника", "")),
                }

                logger.info(
                    f"Собраны данные по комплектации id={config_id}, name={config_name}: {car_data}"
                )

                add_car(config_id, car_data)
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
                continue

    logger.info(
        f"Парсинг автомобилей завершен. Успешно обработано: {len(parsed_cars)} "
        f"из {len(configurations)}"
    )
    return parsed_cars