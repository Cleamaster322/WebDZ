from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from db.brand_crud import add_brand
from parsers import BrowserDriver
from utils.logger import setup_logger


logger = setup_logger(__name__)


def parse_brands(limit=None):
    """Парсинг списка марок с Drom."""
    url = "https://www.drom.ru/catalog/"
    logger.info(f"Старт парсинга марок: {url}, limit={limit}")

    with BrowserDriver() as browser:
        try:
            browser.get(url)
            logger.info("Страница каталога открыта")

            try:
                show_all_button = WebDriverWait(browser.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button[data-ftid="component_cars-list_expand-control"]')
                    )
                )
                show_all_button.click()
                logger.info("Кнопка 'Показать все' найдена и нажата")
            except TimeoutException:
                logger.error("Не удалось найти кнопку 'Показать все'")
                return []

            sleep(2)

            brand_links = browser.driver.find_elements(
                By.CSS_SELECTOR,
                'a[data-ftid="component_cars-list-item_hidden-link"]'
            )

            brands = [
                {
                    "name": el.text.strip(),
                    "link": el.get_attribute("href"),
                }
                for el in brand_links
                if el.text.strip() and el.get_attribute("href")
            ]

            logger.info(f"Всего найдено марок до ограничения: {len(brands)}")

            if limit is not None:
                brands = brands[:limit]
                logger.info(f"После применения limit осталось марок: {len(brands)}")

            for brand in brands:
                try:
                    add_brand(brand["name"], brand["link"])
                    logger.info(
                        f"Марка сохранена/проверена: name={brand['name']}, link={brand['link']}"
                    )
                except Exception as e:
                    logger.error(
                        f"Ошибка при сохранении марки "
                        f"name={brand['name']}, link={brand['link']}: {e}",
                        exc_info=True
                    )

            logger.info("Парсинг марок завершен")
            return brands

        except Exception as e:
            logger.error(f"Ошибка при парсинге марок: {e}", exc_info=True)
            return []