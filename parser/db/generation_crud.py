from db.database import Database
from utils.logger import setup_logger

db = Database()
logger = setup_logger(__name__)


def add_generation(model, generation_data):
    """
    Добавление нового поколения в таблицу generations, если оно ещё не существует.
    Возвращает запись поколения.
    """
    if not model:
        logger.warning(
            "Модель не найдена для поколения: name=%s, link=%s, region=%s",
            generation_data.get("name"),
            generation_data.get("link"),
            generation_data.get("region"),
        )
        return None

    existing_generation = get_generation_by_unique_fields(
        model_id=model["id"],
        generation_num=generation_data.get("generation_num"),
        link=generation_data.get("link"),
        region=generation_data.get("region"),
    )
    if existing_generation:
        logger.info(
            "Поколение уже существует: model_id=%s, model_name=%s, "
            "generation_id=%s, generation_name=%s, region=%s",
            model["id"],
            model["name"],
            existing_generation["id"],
            existing_generation["name"],
            existing_generation.get("region"),
        )
        return existing_generation

    query = """
        INSERT INTO generations (
            model_id,
            name,
            link,
            body_code,
            body_type,
            region,
            image_path,
            is_hybrid,
            generation_num,
            restyling_num,
            date_start,
            date_end
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        model["id"],
        generation_data.get("name"),
        generation_data.get("link"),
        generation_data.get("body_code"),
        generation_data.get("body_type"),
        generation_data.get("region"),
        generation_data.get("image_path"),
        generation_data.get("is_hybrid"),
        generation_data.get("generation_num"),
        generation_data.get("restyling_num"),
        generation_data.get("date_start"),
        generation_data.get("date_end"),
    )

    try:
        generation_id = db.execute_query(query, params)

        created_generation = {
            "id": generation_id,
            "model_id": model["id"],
            "name": generation_data.get("name"),
            "link": generation_data.get("link"),
            "body_code": generation_data.get("body_code"),
            "body_type": generation_data.get("body_type"),
            "region": generation_data.get("region"),
            "image_path": generation_data.get("image_path"),
            "is_hybrid": generation_data.get("is_hybrid"),
            "generation_num": generation_data.get("generation_num"),
            "restyling_num": generation_data.get("restyling_num"),
            "date_start": generation_data.get("date_start"),
            "date_end": generation_data.get("date_end"),
        }

        logger.info(
            "Поколение добавлено: model_id=%s, model_name=%s, generation_id=%s, "
            "generation_name=%s, region=%s, body_type=%s, period=%s-%s",
            model["id"],
            model["name"],
            generation_id,
            generation_data.get("name"),
            generation_data.get("region"),
            generation_data.get("body_type"),
            generation_data.get("date_start"),
            generation_data.get("date_end"),
        )

        return created_generation

    except Exception as e:
        logger.error(
            "Ошибка при добавлении поколения: model_id=%s, model_name=%s, "
            "generation_name=%s, region=%s, error=%s",
            model.get("id"),
            model.get("name"),
            generation_data.get("name"),
            generation_data.get("region"),
            e,
            exc_info=True,
        )
        raise


def update_generation_image_path(generation_id, image_path):
    """Обновляет путь к изображению поколения."""
    query = """
        UPDATE generations
        SET image_path = %s
        WHERE id = %s
    """
    params = (image_path, generation_id)

    try:
        db.execute_query(query, params)
        logger.info(
            "Путь к изображению обновлён: generation_id=%s, image_path=%s",
            generation_id,
            image_path,
        )
    except Exception as e:
        logger.error(
            "Ошибка при обновлении image_path: generation_id=%s, image_path=%s, error=%s",
            generation_id,
            image_path,
            e,
            exc_info=True,
        )
        raise


def is_generation_exists(model_id, generation_num, link, region=None):
    """
    Проверка, существует ли поколение с такими уникальными полями.
    """
    query = """
        SELECT id
        FROM generations
        WHERE model_id = %s
          AND generation_num <=> %s
          AND link = %s
          AND region <=> %s
        LIMIT 1
    """
    params = (model_id, generation_num, link, region)

    try:
        result = db.fetch_all(query, params)
        return bool(result)
    except Exception as e:
        logger.error(
            "Ошибка при проверке существования поколения: "
            "model_id=%s, generation_num=%s, link=%s, region=%s, error=%s",
            model_id,
            generation_num,
            link,
            region,
            e,
            exc_info=True,
        )
        raise


def get_all_generations():
    """Получение всех поколений из таблицы generations."""
    query = """
        SELECT
            id,
            model_id,
            name,
            link,
            body_code,
            body_type,
            region,
            image_path,
            is_hybrid,
            generation_num,
            restyling_num,
            date_start,
            date_end
        FROM generations
    """
    try:
        result = db.fetch_all(query)
        logger.info("Получено поколений из БД: %s", len(result))
        return result
    except Exception as e:
        logger.error("Ошибка при получении всех поколений: %s", e, exc_info=True)
        raise


def get_generation_by_id(generation_id):
    """Получение поколения по ID."""
    query = """
        SELECT
            id,
            model_id,
            name,
            link,
            body_code,
            body_type,
            region,
            image_path,
            is_hybrid,
            generation_num,
            restyling_num,
            date_start,
            date_end
        FROM generations
        WHERE id = %s
        LIMIT 1
    """
    params = (generation_id,)

    try:
        result = db.fetch_all(query, params)
        return result[0] if result else None
    except Exception as e:
        logger.error(
            "Ошибка при получении поколения по ID: generation_id=%s, error=%s",
            generation_id,
            e,
            exc_info=True,
        )
        raise


def get_generation_by_name_and_model(name, model_id):
    """Получение поколения по имени и модели."""
    query = """
        SELECT
            id,
            model_id,
            name,
            link,
            body_code,
            body_type,
            region,
            image_path,
            is_hybrid,
            generation_num,
            restyling_num,
            date_start,
            date_end
        FROM generations
        WHERE name = %s AND model_id = %s
    """
    params = (name, model_id)

    try:
        result = db.fetch_all(query, params)
        return result[0] if result else None
    except Exception as e:
        logger.error(
            "Ошибка при получении поколения по имени и модели: "
            "name=%s, model_id=%s, error=%s",
            name,
            model_id,
            e,
            exc_info=True,
        )
        raise


def get_generation_by_unique_fields(model_id, generation_num, link, region=None):
    """Получение поколения по уникальным полям."""
    query = """
        SELECT
            id,
            model_id,
            name,
            link,
            body_code,
            body_type,
            region,
            image_path,
            is_hybrid,
            generation_num,
            restyling_num,
            date_start,
            date_end
        FROM generations
        WHERE model_id = %s
          AND generation_num <=> %s
          AND link = %s
          AND region <=> %s
        LIMIT 1
    """
    params = (model_id, generation_num, link, region)

    try:
        result = db.fetch_all(query, params)
        return result[0] if result else None
    except Exception as e:
        logger.error(
            "Ошибка при получении поколения по уникальным полям: "
            "model_id=%s, generation_num=%s, link=%s, region=%s, error=%s",
            model_id,
            generation_num,
            link,
            region,
            e,
            exc_info=True,
        )
        raise


def delete_generation(generation_id):
    """Удаление поколения по его ID."""
    query = "DELETE FROM generations WHERE id = %s"
    params = (generation_id,)

    try:
        db.execute_query(query, params)
        logger.info("Поколение удалено: generation_id=%s", generation_id)
    except Exception as e:
        logger.error(
            "Ошибка при удалении поколения: generation_id=%s, error=%s",
            generation_id,
            e,
            exc_info=True,
        )
        raise


def close_db_connection():
    """Закрытие соединения с базой данных."""
    try:
        db.close()
        logger.info("Соединение с БД закрыто в generation_crud")
    except Exception as e:
        logger.error("Ошибка при закрытии соединения с БД: %s", e, exc_info=True)
        raise