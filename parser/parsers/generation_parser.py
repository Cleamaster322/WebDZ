from urllib.parse import urljoin
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from db.generation_crud import add_generation
from utils.logger import setup_logger

BASE_URL = "https://www.drom.ru"

logger = setup_logger(__name__)


def _parse_name_and_dates(text: str) -> tuple[str, str, str]:
    """
    Извлекает name, date_start, date_end из текста заголовка поколения.
    Ожидаемый формат обычно:
        "Название\n2006 - 2008"
    """
    parts = [part.strip() for part in text.split("\n") if part.strip()]

    if not parts:
        return "", "", ""

    name = parts[0]
    date_start = ""
    date_end = ""

    if len(parts) > 1 and " - " in parts[1]:
        date_parts = [part.strip() for part in parts[1].split(" - ", 1)]
        date_start = date_parts[0] if len(date_parts) > 0 else ""
        date_end = date_parts[1] if len(date_parts) > 1 else ""

    return name, date_start, date_end


def _parse_generation_numbers(generation_raw: str) -> tuple[int | None, int]:
    """
    Извлекает номер поколения и номер рестайлинга из строки.
    """
    generation_num = None
    restyling_num = 0

    if not generation_raw:
        return generation_num, restyling_num

    raw_lower = generation_raw.lower()

    first_token = generation_raw.split()[0]
    try:
        generation_num = int(first_token)
    except (ValueError, TypeError):
        generation_num = None

    if "рестайлинг" in raw_lower:
        restyling_num = 1

    return generation_num, restyling_num


def get_media_generations_path() -> str:
    parser_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    project_root = os.path.abspath(os.path.join(parser_dir, ".."))
    media_path = os.path.join(project_root, "main", "media", "generations")

    os.makedirs(media_path, exist_ok=True)
    return media_path


def create_test_generation_file(model: dict, generation_record: dict, generation_data: dict) -> str:
    """
    Создает тестовый файл для поколения в формате:
    brandId_modelId_generationId.txt
    """
    media_path = get_media_generations_path()

    brand_id = model["brand_id"]
    model_id = model["id"]
    generation_id = generation_record["id"]

    file_name = f"{brand_id}_{model_id}_{generation_id}.txt"
    file_path = os.path.join(media_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(
            "TEST GENERATION FILE\n"
            f"brand_id={brand_id}\n"
            f"model_id={model_id}\n"
            f"generation_id={generation_id}\n"
            f"model_name={model.get('name')}\n"
            f"generation_name={generation_data.get('name')}\n"
            f"date_start={generation_data.get('date_start')}\n"
            f"date_end={generation_data.get('date_end')}\n"
            f"link={generation_data.get('link')}\n"
        )

    return file_path


def parse_generation(models, browser):
    logger.info("Старт parse_generation")

    for model in models:
        model_id = model.get("id")
        model_name = model.get("name")
        model_link = model.get("link")
        brand_id = model.get("brand_id")

        if not model_link:
            logger.warning(
                f"У модели отсутствует link: id={model_id}, name={model_name}"
            )
            continue

        if brand_id is None:
            logger.warning(
                f"У модели отсутствует brand_id: id={model_id}, name={model_name}"
            )
            continue

        try:
            logger.info(
                f"Обработка модели: id={model_id}, name={model_name}, link={model_link}"
            )
            browser.get(model_link)

            try:
                russia_block = WebDriverWait(browser.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "russia"))
                )
            except TimeoutException:
                logger.warning(
                    f'Нет блока с ID="russia" для модели: id={model_id}, name={model_name}'
                )
                continue

            try:
                generations_block = russia_block.find_element(
                    By.XPATH,
                    "following-sibling::div[1]"
                )
            except Exception as e:
                logger.error(
                    f"Не удалось найти блок поколений после #russia "
                    f"для модели id={model_id}, name={model_name}: {e}",
                    exc_info=True
                )
                continue

            generation_elements = generations_block.find_elements(
                By.XPATH,
                ".//a[@data-ftid='component_article']"
            )

            if not generation_elements:
                logger.warning(
                    f"Для модели id={model_id}, name={model_name} поколения не найдены"
                )
                continue

            logger.info(
                f"Найдено поколений для модели id={model_id}, name={model_name}: "
                f"{len(generation_elements)}"
            )

            for el in generation_elements:
                try:
                    href = el.get_attribute("href")
                    link = urljoin(BASE_URL, href) if href else ""

                    name_elem = el.find_element(
                        By.XPATH,
                        './/span[@data-ftid="component_article_caption"]'
                    )
                    raw_caption = name_elem.text.strip()

                    name, date_start, date_end = _parse_name_and_dates(raw_caption)

                    info_divs = el.find_elements(
                        By.XPATH,
                        './/div[@data-ftid="component_article_extended-info"]/div'
                    )

                    generation_raw = info_divs[0].text.strip() if len(info_divs) > 0 else ""
                    body_code = info_divs[1].text.strip() if len(info_divs) > 1 else ""
                    body_type = info_divs[2].text.strip() if len(info_divs) > 2 else ""

                    generation_num, restyling_num = _parse_generation_numbers(generation_raw)

                    is_hybrid = "гибрид" in body_type.lower()
                    body_type = (
                        body_type
                        .replace(", Гибрид", "")
                        .replace(", гибрид", "")
                        .strip()
                    )

                    generation = {
                        "name": name,
                        "date_start": date_start,
                        "date_end": date_end,
                        "link": link,
                        "body_code": body_code,
                        "body_type": body_type,
                        "is_hybrid": is_hybrid,
                        "generation_num": generation_num,
                        "restyling_num": restyling_num,
                    }

                    logger.info(
                        f"Добавление поколения для модели id={model_id}, "
                        f"name={model_name}: {generation}"
                    )

                    generation_record = add_generation(model, generation)

                    if not generation_record:
                        logger.warning(
                            f"Не удалось получить запись поколения после сохранения: "
                            f"model_id={model_id}, model_name={model_name}, generation_name={generation['name']}"
                        )
                        continue

                    file_path = create_test_generation_file(
                        model=model,
                        generation_record=generation_record,
                        generation_data=generation,
                    )

                    logger.info(f"Создан тестовый файл: {file_path}")

                except Exception as gen_err:
                    logger.error(
                        f"Ошибка при разборе поколения для модели "
                        f"id={model_id}, name={model_name}: {gen_err}",
                        exc_info=True
                    )
                    continue

        except Exception as e:
            logger.error(
                f"Ошибка при обработке модели id={model_id}, name={model_name}: {e}",
                exc_info=True
            )
            continue

    logger.info("Завершение parse_generation")