from db.database import Database
from .brand_crud import get_brand_by_name
from utils.logger import setup_logger

db = Database()
logger = setup_logger(__name__)


def add_model(brand_name, model_name, model_link):
    """Добавление новой модели в таблицу models, если она ещё не существует."""
    brand = get_brand_by_name(brand_name)

    if not brand:
        logger.warning(
            f"Марка '{brand_name}' не найдена. Модель '{model_name}' не добавлена."
        )
        return False

    if is_model_exists(brand["id"], model_name, model_link):
        logger.info(
            f"Модель '{model_name}' для марки '{brand_name}' уже существует в базе данных."
        )
        return False

    query = "INSERT INTO models (brand_id, name, link) VALUES (%s, %s, %s)"
    params = (brand["id"], model_name, model_link)
    db.execute_query(query, params)

    logger.info(
        f"Модель '{model_name}' для марки '{brand_name}' успешно добавлена в базу данных."
    )
    return True


def is_model_exists(brand_id, name, link):
    """Проверка, существует ли модель с таким названием и ссылкой для данной марки."""
    query = """
        SELECT id
        FROM models
        WHERE brand_id = %s AND name = %s AND link = %s
    """
    params = (brand_id, name, link)
    result = db.fetch_all(query, params)
    return len(result) > 0


def get_all_models():
    """Получение всех моделей из таблицы models с именем бренда."""
    query = """
        SELECT
            m.id,
            m.brand_id,
            m.name,
            m.link,
            b.name AS brand_name
        FROM models m
        JOIN brands b ON b.id = m.brand_id
    """
    models = db.fetch_all(query)
    logger.info(f"Получено моделей из БД: {len(models)}")
    return models


def get_model_by_name(name):
    """
    Получение модели по имени.
    Использовать с осторожностью: имя модели может быть не уникально глобально.
    """
    query = """
        SELECT id, brand_id, name, link
        FROM models
        WHERE name = %s
    """
    params = (name,)
    result = db.fetch_all(query, params)
    return result[0] if result else None


def get_model_by_name_and_brand(name, brand_id):
    """Получение модели по имени и ID марки."""
    query = """
        SELECT id, brand_id, name, link
        FROM models
        WHERE name = %s AND brand_id = %s
    """
    params = (name, brand_id)
    result = db.fetch_all(query, params)
    return result[0] if result else None


def update_model_link(model_id, new_link):
    """Обновление ссылки на модель по её ID."""
    query = "UPDATE models SET link = %s WHERE id = %s"
    params = (new_link, model_id)
    db.execute_query(query, params)
    logger.info(f"Ссылка модели с id={model_id} обновлена.")


def delete_model(model_id):
    """Удаление модели по её ID."""
    query = "DELETE FROM models WHERE id = %s"
    params = (model_id,)
    db.execute_query(query, params)
    logger.info(f"Модель с id={model_id} удалена.")


def close_db_connection():
    """Закрытие соединения с базой данных."""
    db.close()
    logger.info("Соединение с БД в models_crud закрыто.")