from selenium.webdriver.common.by import By

from db.models_crud import add_model
from utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_models(brand, browser):
    """Парсинг моделей для одной марки."""
    try:
        logger.info(f"Открываем страницу бренда: {brand['name']}")

        browser.get(brand["link"])

        model_links = browser.driver.find_elements(
            By.CSS_SELECTOR,
            'a.g6gv8w4.g6gv8w8._501ok20'
        )

        if not model_links:
            logger.warning(f"Не найдено ни одной модели для бренда: {brand['name']}")
            return []

        models = [
            {
                "name": el.text.strip(),
                "link": el.get_attribute("href"),
            }
            for el in model_links
            if el.text.strip() and el.get_attribute("href")
        ]

        logger.info(f"Найдено моделей: {len(models)} для бренда {brand['name']}")

        for model in models:
            try:
                logger.info(f"Добавляем модель: {model['name']} ({brand['name']})")
                add_model(brand["name"], model["name"], model["link"])
            except Exception as e:
                logger.error(
                    f"Ошибка при добавлении модели {model['name']} "
                    f"для бренда {brand['name']}: {e}",
                    exc_info=True
                )
                continue

        return models

    except Exception as e:
        logger.error(
            f"Ошибка при парсинге моделей марки {brand['name']}: {e}",
            exc_info=True
        )
        return []