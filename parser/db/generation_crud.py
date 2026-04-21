from db.database import Database
from utils.logger import setup_logger

db = Database()
logger = setup_logger(__name__)


def add_generation(model, generation_data):
    """Добавление нового поколения в таблицу generations, если оно ещё не существует.
    Возвращает запись поколения.
    """
    if not model:
        logger.warning(
            "Модель не найдена для поколения: name=%s, link=%s",
            generation_data.get("name"),
            generation_data.get("link"),
        )
        return None

    existing_generation = get_generation_by_unique_fields(
        model["id"],
        generation_data["generation_num"],
        generation_data["link"]
    )
    if existing_generation:
        logger.info(
            "Поколение уже существует: model_id=%s, model_name=%s, generation_id=%s, generation_name=%s",
            model["id"],
            model["name"],
            existing_generation["id"],
            existing_generation["name"],
        )
        return existing_generation

    query = """
        INSERT INTO generations (
            model_id,
            name,
            link,
            body_code,
            body_type,
            is_hybrid,
            generation_num,
            restyling_num,
            date_start,
            date_end
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        model["id"],
        generation_data["name"],
        generation_data["link"],
        generation_data["body_code"],
        generation_data["body_type"],
        generation_data["is_hybrid"],
        generation_data["generation_num"],
        generation_data["restyling_num"],
        generation_data["date_start"],
        generation_data["date_end"],
    )

    try:
        db.execute_query(query, params)
        logger.info(
            "Поколение добавлено: model_id=%s, model_name=%s, generation_name=%s, "
            "body_type=%s, period=%s-%s",
            model["id"],
            model["name"],
            generation_data["name"],
            generation_data["body_type"],
            generation_data["date_start"],
            generation_data["date_end"],
        )

        created_generation = get_generation_by_unique_fields(
            model["id"],
            generation_data["generation_num"],
            generation_data["link"]
        )
        return created_generation

    except Exception as e:
        logger.error(
            "Ошибка при добавлении поколения: model_id=%s, model_name=%s, "
            "generation_name=%s, error=%s",
            model.get("id"),
            model.get("name"),
            generation_data.get("name"),
            e,
            exc_info=True,
        )
        raise


def is_generation_exists(model_id, generation_number, link):
    """Проверка, существует ли поколение с таким номером и ссылкой для данной модели."""
    query = """
        SELECT id
        FROM generations
        WHERE model_id = %s AND generation_num = %s AND link = %s
    """
    params = (model_id, generation_number, link)

    try:
        result = db.fetch_all(query, params)
        return bool(result)
    except Exception as e:
        logger.error(
            "Ошибка при проверке существования поколения: model_id=%s, generation_num=%s, "
            "link=%s, error=%s",
            model_id,
            generation_number,
            link,
            e,
            exc_info=True,
        )
        raise


def get_all_generations():
    """Получение всех поколений из таблицы generations."""
    query = """
        SELECT id, model_id, name, link, body_code, body_type,
               is_hybrid, generation_num, restyling_num, date_start, date_end
        FROM generations
    """
    try:
        result = db.fetch_all(query)
        logger.info("Получено поколений из БД: %s", len(result))
        return result
    except Exception as e:
        logger.error("Ошибка при получении всех поколений: %s", e, exc_info=True)
        raise


def get_generation_by_name_and_model(name, model_id):
    """Получение поколения по имени и модели."""
    query = """
        SELECT id, model_id, name, link, body_code, body_type,
               is_hybrid, generation_num, restyling_num, date_start, date_end
        FROM generations
        WHERE name = %s AND model_id = %s
    """
    params = (name, model_id)

    try:
        result = db.fetch_all(query, params)
        return result[0] if result else None
    except Exception as e:
        logger.error(
            "Ошибка при получении поколения по имени и модели: name=%s, model_id=%s, error=%s",
            name,
            model_id,
            e,
            exc_info=True,
        )
        raise


def get_generation_by_unique_fields(model_id, generation_num, link):
    """Получение поколения по уникальным полям."""
    query = """
        SELECT id, model_id, name, link, body_code, body_type,
               is_hybrid, generation_num, restyling_num, date_start, date_end
        FROM generations
        WHERE model_id = %s AND generation_num = %s AND link = %s
        LIMIT 1
    """
    params = (model_id, generation_num, link)

    try:
        result = db.fetch_all(query, params)
        return result[0] if result else None
    except Exception as e:
        logger.error(
            "Ошибка при получении поколения по уникальным полям: "
            "model_id=%s, generation_num=%s, link=%s, error=%s",
            model_id,
            generation_num,
            link,
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