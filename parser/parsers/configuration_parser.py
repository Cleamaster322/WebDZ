from selenium.webdriver.common.by import By

from .driver import BrowserDriver
from db.configuration_crud import add_configuration
from utils.logger import setup_logger

logger = setup_logger(__name__)


def is_number(value):
    """Проверка, является ли строка числом."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def parse_release_period(release_period: str) -> tuple[str, str]:
    """
    Разбирает период выпуска вида '2006-2008' или '2006-'.
    Возвращает (date_start, date_end).
    """
    cleaned = (release_period or "").strip().replace(" ", "")

    if not cleaned:
        return "", ""

    if "-" not in cleaned:
        logger.warning(f"Нестандартный формат периода выпуска: '{release_period}'")
        return cleaned, ""

    parts = cleaned.split("-", 1)
    date_start = parts[0].strip()
    date_end = parts[1].strip() if len(parts) > 1 else ""

    if date_end == "":
        date_end = "н.в."

    return date_start, date_end


def parse_configurations(generations):
    """Парсинг комплектаций для заданных поколений."""
    logger.info(f"Запуск парсинга комплектаций. Поколений к обработке: {len(generations)}")

    with BrowserDriver() as browser:
        for generation in generations:
            generation_id = generation.get("id")
            generation_name = generation.get("name", "Без названия")
            generation_link = generation.get("link")

            try:
                if not generation_link:
                    logger.warning(
                        f"У поколения отсутствует ссылка: id={generation_id}, name={generation_name}"
                    )
                    continue

                logger.info(
                    f"Обработка поколения: id={generation_id}, name={generation_name}, link={generation_link}"
                )

                browser.get(generation_link)

                configuration_rows = browser.driver.find_elements(
                    By.CSS_SELECTOR,
                    'tr[data-ftid="complectations-table-row"]'
                )

                logger.info(
                    f"Для поколения id={generation_id}, name={generation_name} "
                    f"найдено строк комплектаций: {len(configuration_rows)}"
                )

                if not configuration_rows:
                    logger.warning(
                        f"Для поколения id={generation_id}, name={generation_name} "
                        f"не найдено ни одной строки комплектации"
                    )
                    continue

                for row_index, row in enumerate(configuration_rows, start=1):
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")

                        if len(cells) < 3:
                            logger.warning(
                                f"Слишком мало ячеек в строке комплектации "
                                f"(generation_id={generation_id}, generation_name={generation_name}, row={row_index})"
                            )
                            continue

                        shift = 0

                        name = cells[1].text.strip()
                        if not name:
                            logger.warning(
                                f"Пустое имя комплектации "
                                f"(generation_id={generation_id}, generation_name={generation_name}, row={row_index})"
                            )
                            continue

                        links = cells[1].find_elements(By.TAG_NAME, "a")
                        if not links:
                            logger.warning(
                                f"Не найдена ссылка у комплектации '{name}' "
                                f"(generation_id={generation_id}, row={row_index})"
                            )
                            continue

                        link = links[0].get_attribute("href")
                        if not link:
                            logger.warning(
                                f"Пустой href у комплектации '{name}' "
                                f"(generation_id={generation_id}, row={row_index})"
                            )
                            continue

                        release_period = cells[2].text.strip()
                        date_start, date_end = parse_release_period(release_period)

                        if len(cells) > 3 and not is_number(cells[3].text.strip().replace(" ", "")):
                            shift = -1

                        engine_index = 4 + shift
                        engine_name = cells[engine_index].text.strip() if len(cells) > engine_index else ""

                        if engine_name == "Сравнить":
                            engine_name = ""

                        configuration = {
                            "name": name,
                            "link": link,
                            "date_start": date_start,
                            "date_end": date_end,
                            "engine_name": engine_name,
                        }

                        logger.info(
                            f"Сохранение комплектации: "
                            f"generation_id={generation_id}, name={name}, "
                            f"date_start={date_start}, date_end={date_end}, engine_name={engine_name}"
                        )

                        add_configuration(generation_id, configuration)

                    except Exception as e:
                        logger.error(
                            f"Ошибка при парсинге комплектации "
                            f"(generation_id={generation_id}, generation_name={generation_name}, row={row_index}): {e}",
                            exc_info=True
                        )
                        continue

            except Exception as e:
                logger.error(
                    f"Ошибка при обработке поколения "
                    f"id={generation_id}, name={generation_name}: {e}",
                    exc_info=True
                )
                continue

    logger.info("Парсинг комплектаций завершен")