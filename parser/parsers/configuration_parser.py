from selenium.webdriver.common.by import By

from db.configuration_crud import add_configuration
from parsers.error_writer import write_parser_error
from utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_release_period(release_period: str) -> tuple[str, str]:
    cleaned = (release_period or "").strip()

    if not cleaned:
        return "", ""

    parts = [p.strip() for p in cleaned.split("-", 1)]

    if len(parts) == 1:
        logger.warning(f"Нестандартный формат периода выпуска: '{release_period}'")
        write_parser_error(
            "CONFIG_RELEASE_PERIOD_UNEXPECTED_FORMAT",
            {
                "release_period": release_period,
            },
        )
        return parts[0], ""

    date_start = parts[0]
    date_end = parts[1]

    if not date_end:
        date_end = "н.в."

    return date_start, date_end


def extract_engine_info_from_tbody(tbody):
    engine_name = ""
    engine_group_text = ""

    try:
        summary_elements = tbody.find_elements(By.CSS_SELECTOR, "div.r6hmq22")
        if summary_elements:
            engine_group_text = summary_elements[0].text.strip()
    except Exception:
        pass

    try:
        engine_links = tbody.find_elements(By.CSS_SELECTOR, "span._13wmddp2 a")
        if engine_links:
            engine_name = engine_links[0].text.strip()
    except Exception:
        pass

    return engine_name, engine_group_text


def extract_configuration_from_row(
    row,
    engine_name,
    generation_id,
    generation_name,
    generation_link,
    page_url,
    tbody_index,
    row_index,
):
    cells = row.find_elements(By.TAG_NAME, "td")

    if len(cells) < 3:
        logger.warning(
            f"Слишком мало ячеек в строке комплектации "
            f"(generation_id={generation_id}, generation_name={generation_name}, "
            f"page_url={page_url}, tbody={tbody_index}, row={row_index}, cells_count={len(cells)})"
        )
        write_parser_error(
            "CONFIG_ROW_TOO_FEW_CELLS",
            {
                "generation_id": generation_id,
                "generation_name": generation_name,
                "generation_link": generation_link,
                "page_url": page_url,
                "tbody_index": tbody_index,
                "row_index": row_index,
                "cells_count": len(cells),
            },
        )
        return None

    name_cell = cells[1]

    link_elements = name_cell.find_elements(By.TAG_NAME, "a")
    if not link_elements:
        logger.warning(
            f"Не найдена ссылка у строки комплектации "
            f"(generation_id={generation_id}, generation_name={generation_name}, "
            f"page_url={page_url}, tbody={tbody_index}, row={row_index})"
        )
        write_parser_error(
            "CONFIG_LINK_MISSING",
            {
                "generation_id": generation_id,
                "generation_name": generation_name,
                "generation_link": generation_link,
                "page_url": page_url,
                "tbody_index": tbody_index,
                "row_index": row_index,
            },
        )
        return None

    link_element = link_elements[0]
    name = link_element.text.strip()
    link = link_element.get_attribute("href")

    if not name:
        logger.warning(
            f"Пустое имя комплектации "
            f"(generation_id={generation_id}, generation_name={generation_name}, "
            f"page_url={page_url}, tbody={tbody_index}, row={row_index})"
        )
        write_parser_error(
            "CONFIG_NAME_MISSING",
            {
                "generation_id": generation_id,
                "generation_name": generation_name,
                "generation_link": generation_link,
                "page_url": page_url,
                "tbody_index": tbody_index,
                "row_index": row_index,
            },
        )
        return None

    if not link:
        logger.warning(
            f"Пустой href у комплектации '{name}' "
            f"(generation_id={generation_id}, generation_name={generation_name}, "
            f"page_url={page_url}, tbody={tbody_index}, row={row_index})"
        )
        write_parser_error(
            "CONFIG_LINK_MISSING",
            {
                "generation_id": generation_id,
                "generation_name": generation_name,
                "generation_link": generation_link,
                "page_url": page_url,
                "tbody_index": tbody_index,
                "row_index": row_index,
                "configuration_name": name,
            },
        )
        return None

    release_period = cells[2].text.strip()
    date_start, date_end = parse_release_period(release_period)

    configuration = {
        "name": name,
        "link": link,
        "date_start": date_start,
        "date_end": date_end,
        "engine_name": engine_name,
    }

    return configuration


def get_next_page_url(browser):
    """
    Возвращает ссылку на следующую страницу комплектаций или None.
    """
    try:
        next_links = browser.driver.find_elements(
            By.CSS_SELECTOR,
            'a[data-ftid="component_pagination-item-next"]'
        )

        if not next_links:
            return None

        next_url = next_links[0].get_attribute("href")
        return next_url if next_url else None
    except Exception:
        return None


def parse_configurations(generations, browser):
    logger.info(
        f"Запуск парсинга комплектаций. Поколений к обработке: {len(generations)}"
    )

    generations_total = len(generations)
    generations_processed = 0
    generations_without_table = 0
    configurations_saved = 0
    row_errors = 0

    for generation in generations:
        generation_id = generation.get("id")
        generation_name = generation.get("name", "Без названия")
        generation_link = generation.get("link")

        try:
            if not generation_link:
                logger.warning(
                    f"У поколения отсутствует ссылка: id={generation_id}, name={generation_name}"
                )
                write_parser_error(
                    "GENERATION_LINK_MISSING",
                    {
                        "generation_id": generation_id,
                        "generation_name": generation_name,
                    },
                )
                continue

            logger.info(
                f"Обработка поколения: id={generation_id}, name={generation_name}, link={generation_link}"
            )

            total_rows = 0
            visited_pages = set()
            current_page_url = generation_link
            page_number = 1
            found_any_table = False

            while current_page_url:
                if current_page_url in visited_pages:
                    logger.warning(
                        f"Обнаружен повтор страницы пагинации, остановка "
                        f"(generation_id={generation_id}, generation_name={generation_name}, page_url={current_page_url})"
                    )
                    write_parser_error(
                        "CONFIG_PAGINATION_LOOP_DETECTED",
                        {
                            "generation_id": generation_id,
                            "generation_name": generation_name,
                            "generation_link": generation_link,
                            "page_url": current_page_url,
                        },
                    )
                    break

                visited_pages.add(current_page_url)

                logger.info(
                    f"Открытие страницы комплектаций #{page_number}: "
                    f"(generation_id={generation_id}, generation_name={generation_name}, page_url={current_page_url})"
                )

                browser.get(current_page_url)

                table_elements = browser.driver.find_elements(
                    By.CSS_SELECTOR,
                    'div[data-app-root="catalog-complectations-table"] table.qn4xij0',
                )

                if not table_elements:
                    logger.warning(
                        f"Не найдена таблица комплектаций "
                        f"(generation_id={generation_id}, generation_name={generation_name}, page_url={current_page_url})"
                    )
                    write_parser_error(
                        "CONFIG_TABLE_NOT_FOUND",
                        {
                            "generation_id": generation_id,
                            "generation_name": generation_name,
                            "generation_link": generation_link,
                            "page_url": current_page_url,
                        },
                    )

                    if page_number == 1:
                        generations_without_table += 1
                    break

                found_any_table = True
                table = table_elements[0]
                tbodies = table.find_elements(By.TAG_NAME, "tbody")

                logger.info(
                    f"Для поколения id={generation_id}, name={generation_name}, page={page_number} "
                    f"найдено групп комплектаций (tbody): {len(tbodies)}"
                )

                if not tbodies:
                    logger.warning(
                        f"Для поколения id={generation_id}, name={generation_name}, page={page_number} "
                        f"не найдено ни одной группы комплектаций"
                    )
                    write_parser_error(
                        "CONFIG_TBODY_EMPTY",
                        {
                            "generation_id": generation_id,
                            "generation_name": generation_name,
                            "generation_link": generation_link,
                            "page_url": current_page_url,
                        },
                    )
                    break

                for tbody_index, tbody in enumerate(tbodies, start=1):
                    try:
                        engine_name, engine_group_text = extract_engine_info_from_tbody(tbody)

                        if not engine_name:
                            error_type = "CONFIG_ENGINE_CODE_MISSING"
                            group_text_lower = engine_group_text.lower()

                            if "электричество" in group_text_lower:
                                error_type = "CONFIG_ENGINE_CODE_NOT_APPLICABLE_EV"

                            logger.warning(
                                f"Не найден код двигателя в группе комплектаций "
                                f"(generation_id={generation_id}, generation_name={generation_name}, "
                                f"page={page_number}, tbody={tbody_index}, group_text={engine_group_text})"
                            )

                            write_parser_error(
                                error_type,
                                {
                                    "generation_id": generation_id,
                                    "generation_name": generation_name,
                                    "generation_link": generation_link,
                                    "page_url": current_page_url,
                                    "tbody_index": tbody_index,
                                    "engine_group_text": engine_group_text,
                                },
                            )

                        rows = tbody.find_elements(By.CSS_SELECTOR, "tr.y7l57t2")

                        logger.info(
                            f"Группа {tbody_index}: engine_name={engine_name}, строк комплектаций={len(rows)} "
                            f"(generation_id={generation_id}, generation_name={generation_name}, page={page_number})"
                        )

                        if not rows:
                            write_parser_error(
                                "CONFIG_GROUP_ROWS_EMPTY",
                                {
                                    "generation_id": generation_id,
                                    "generation_name": generation_name,
                                    "generation_link": generation_link,
                                    "page_url": current_page_url,
                                    "tbody_index": tbody_index,
                                    "engine_name": engine_name,
                                    "engine_group_text": engine_group_text,
                                },
                            )

                        for row_index, row in enumerate(rows, start=1):
                            try:
                                configuration = extract_configuration_from_row(
                                    row=row,
                                    engine_name=engine_name,
                                    generation_id=generation_id,
                                    generation_name=generation_name,
                                    generation_link=generation_link,
                                    page_url=current_page_url,
                                    tbody_index=tbody_index,
                                    row_index=row_index,
                                )

                                if not configuration:
                                    row_errors += 1
                                    continue

                                logger.info(
                                    f"Сохранение комплектации: "
                                    f"generation_id={generation_id}, name={configuration['name']}, "
                                    f"date_start={configuration['date_start']}, "
                                    f"date_end={configuration['date_end']}, "
                                    f"engine_name={configuration['engine_name']}, "
                                    f"link={configuration['link']}"
                                )

                                add_configuration(generation_id, configuration)
                                total_rows += 1
                                configurations_saved += 1

                            except Exception as e:
                                logger.error(
                                    f"Ошибка при парсинге комплектации "
                                    f"(generation_id={generation_id}, generation_name={generation_name}, "
                                    f"page={page_number}, tbody={tbody_index}, row={row_index}): {e}",
                                    exc_info=True,
                                )
                                write_parser_error(
                                    "CONFIG_ROW_PARSE_ERROR",
                                    {
                                        "generation_id": generation_id,
                                        "generation_name": generation_name,
                                        "generation_link": generation_link,
                                        "page_url": current_page_url,
                                        "tbody_index": tbody_index,
                                        "row_index": row_index,
                                        "error": str(e),
                                    },
                                )
                                row_errors += 1
                                continue

                    except Exception as e:
                        logger.error(
                            f"Ошибка при обработке группы комплектаций "
                            f"(generation_id={generation_id}, generation_name={generation_name}, "
                            f"page={page_number}, tbody={tbody_index}): {e}",
                            exc_info=True,
                        )
                        write_parser_error(
                            "CONFIG_GROUP_PARSE_ERROR",
                            {
                                "generation_id": generation_id,
                                "generation_name": generation_name,
                                "generation_link": generation_link,
                                "page_url": current_page_url,
                                "tbody_index": tbody_index,
                                "error": str(e),
                            },
                        )
                        continue

                next_page_url = get_next_page_url(browser)

                if next_page_url:
                    logger.info(
                        f"Найдена следующая страница комплектаций: "
                        f"(generation_id={generation_id}, generation_name={generation_name}, next_page_url={next_page_url})"
                    )
                    current_page_url = next_page_url
                    page_number += 1
                else:
                    current_page_url = None

            if not found_any_table:
                logger.warning(
                    f"Для поколения id={generation_id}, name={generation_name} не удалось обработать ни одной страницы таблицы"
                )

            logger.info(
                f"Для поколения id={generation_id}, name={generation_name} "
                f"всего обработано комплектаций: {total_rows}"
            )
            generations_processed += 1

        except Exception as e:
            logger.error(
                f"Ошибка при обработке поколения "
                f"id={generation_id}, name={generation_name}: {e}",
                exc_info=True,
            )
            write_parser_error(
                "CONFIG_GENERATION_PARSE_ERROR",
                {
                    "generation_id": generation_id,
                    "generation_name": generation_name,
                    "generation_link": generation_link,
                    "error": str(e),
                },
            )
            generations_processed += 1
            continue

    logger.info("Парсинг комплектаций завершен")
    logger.info(
        "Итог этапа configurations: поколений всего=%s, обработано=%s, без таблицы=%s, "
        "сохранено конфигураций=%s, ошибок строк=%s",
        generations_total,
        generations_processed,
        generations_without_table,
        configurations_saved,
        row_errors,
    )