import argparse

from utils.logger import setup_logger
from parsers import (
    brand_parser as BP,
    model_parser as MP,
    generation_parser as GP,
    configuration_parser as CP,
    car_parser as CarP,
    BrowserDriver,
)

from db.brand_crud import get_all_brands
from db.models_crud import get_all_models
from db.generation_crud import get_all_generations
from db.configuration_crud import get_all_configurations

logger = setup_logger(__name__)


def run_brands(limit=None, brand_name=None, model_name=None, generation_id=None):
    logger.info(
        f"Запуск этапа brands (limit={limit}, brand={brand_name}, model={model_name}, generation_id={generation_id})"
    )
    BP.parse_brands(limit=limit)
    logger.info("Этап brands завершен")


def run_models(limit=None, brand_name=None, model_name=None, generation_id=None):
    logger.info(
        f"Запуск этапа models (limit={limit}, brand={brand_name}, model={model_name}, generation_id={generation_id})"
    )

    brands = get_all_brands()
    if not brands:
        logger.warning("В таблице brands нет данных")
        return

    if brand_name:
        brands = [
            b for b in brands
            if b.get("name", "").lower() == brand_name.lower()
        ]

    if limit is not None:
        brands = brands[:limit]

    if not brands:
        logger.warning("После фильтрации не осталось брендов")
        return

    with BrowserDriver() as browser:
        for brand in brands:
            MP.parse_models(brand, browser)

    logger.info("Этап models завершен")


def run_generations(limit=None, brand_name=None, model_name=None, generation_id=None):
    logger.info(
        f"Запуск этапа generations (limit={limit}, brand={brand_name}, model={model_name}, generation_id={generation_id})"
    )

    models = get_all_models()
    if not models:
        logger.warning("В таблице models нет данных")
        return

    if brand_name:
        models = [
            m for m in models
            if m.get("brand_name", "").lower() == brand_name.lower()
        ]

    if model_name:
        models = [
            m for m in models
            if m.get("name", "").lower() == model_name.lower()
        ]

    if limit is not None:
        models = models[:limit]

    if not models:
        logger.warning("После фильтрации не осталось моделей")
        return

    with BrowserDriver() as browser:
        GP.parse_generation(models, browser)

    logger.info("Этап generations завершен")


def run_configurations(limit=None, brand_name=None, model_name=None, generation_id=None):
    logger.info(
        f"Запуск этапа configurations (limit={limit}, brand={brand_name}, model={model_name}, generation_id={generation_id})"
    )

    generations = get_all_generations()
    if not generations:
        logger.warning("В таблице generations нет данных")
        return

    if brand_name:
        generations = [
            g for g in generations
            if g.get("brand_name", "").lower() == brand_name.lower()
        ]

    if model_name:
        generations = [
            g for g in generations
            if g.get("model_name", "").lower() == model_name.lower()
        ]

    if generation_id is not None:
        generations = [
            g for g in generations
            if g.get("id") == generation_id
        ]

    if limit is not None:
        generations = generations[:limit]

    if not generations:
        logger.warning("После фильтрации не осталось поколений")
        return

    with BrowserDriver() as browser:
        CP.parse_configurations(generations, browser)

    logger.info("Этап configurations завершен")


def run_cars(limit=None, brand_name=None, model_name=None, generation_id=None, configuration_id=None):
    logger.info(
        f"Запуск этапа cars (limit={limit}, brand={brand_name}, model={model_name}, generation_id={generation_id})"
    )

    configs = get_all_configurations()
    if not configs:
        logger.warning("В таблице configurations нет данных")
        return

    if brand_name:
        configs = [
            c for c in configs
            if c.get("brand_name", "").lower() == brand_name.lower()
        ]

    if model_name:
        configs = [
            c for c in configs
            if c.get("model_name", "").lower() == model_name.lower()
        ]

    if generation_id is not None:
        configs = [
            c for c in configs
            if c.get("generation_id") == generation_id
        ]

    if configuration_id is not None:
        configs = [
            c for c in configs
            if c.get("id") == configuration_id
        ]

    if limit is not None:
        configs = configs[:limit]

    if not configs:
        logger.warning("После фильтрации не осталось комплектаций")
        return

    CarP.parse_cars(configs)
    logger.info("Этап cars завершен")

STAGES = {
    "brands": run_brands,
    "models": run_models,
    "generations": run_generations,
    "configurations": run_configurations,
    "cars": run_cars,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Drom.ru parser — запуск нужного этапа выгрузки"
    )

    parser.add_argument(
        "--stage",
        choices=STAGES.keys(),
        required=True,
        help="Этап: brands | models | generations | configurations | cars",
    )

    parser.add_argument(
        "--limit",
        type=int,
        required=False,
        help="Ограничение количества записей (для тестирования)",
    )

    parser.add_argument(
        "--brand",
        type=str,
        required=False,
        help="Фильтр по марке",
    )

    parser.add_argument(
        "--model",
        type=str,
        required=False,
        help="Фильтр по модели",
    )

    parser.add_argument(
        "--generation-id",
        type=int,
        required=False,
        help="Фильтр по ID поколения",
    )
    parser.add_argument(
        "--configuration-id",
        type=int,
        required=False,
        help="Фильтр по ID комплектации",
    )

    args = parser.parse_args()

    try:
        logger.info(
            f"Выбран этап: {args.stage}, limit={args.limit}, brand={args.brand}, model={args.model}, generation_id={args.generation_id}"
        )

        STAGES[args.stage](
            limit=args.limit,
            brand_name=args.brand,
            model_name=args.model,
            generation_id=args.generation_id,
            configuration_id=args.configuration_id,
        )

    except Exception as e:
        logger.error(
            f"Критическая ошибка на этапе {args.stage}: {e}",
            exc_info=True,
        )
        raise


if __name__ == "__main__":
    main()