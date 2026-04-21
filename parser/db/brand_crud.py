from db.database import Database
from utils.logger import setup_logger

logger = setup_logger(__name__)
db = Database()


def add_brand(name, link):
    """Добавление новой марки в таблицу brands, если она ещё не существует."""
    if is_brand_exists(name, link):
        logger.warning(f"Марка уже существует: name={name}, link={link}")
        return

    query = "INSERT INTO brands (name, link) VALUES (%s, %s)"
    params = (name, link)
    db.execute_query(query, params)
    logger.info(f"Марка добавлена: name={name}, link={link}")


def is_brand_exists(name, link):
    """Проверка, существует ли марка с таким названием и ссылкой."""
    query = """
        SELECT id
        FROM brands
        WHERE name = %s AND link = %s
    """
    params = (name, link)
    result = db.fetch_all(query, params)
    return len(result) > 0


def get_all_brands():
    """Получение всех марок из таблицы brands."""
    query = "SELECT id, name, link FROM brands"
    brands = db.fetch_all(query)
    logger.info(f"Получено марок из БД: {len(brands)}")
    return brands


def get_brand_by_name(name):
    """Получение марки по имени."""
    query = """
        SELECT id, name, link
        FROM brands
        WHERE name = %s
    """
    params = (name,)
    result = db.fetch_all(query, params)

    if result:
        logger.info(f"Марка найдена по имени: name={name}, id={result[0]['id']}")
        return result[0]

    logger.warning(f"Марка не найдена по имени: name={name}")
    return None


def update_brand_link(brand_id, new_link):
    """Обновление ссылки на марку по её ID."""
    query = "UPDATE brands SET link = %s WHERE id = %s"
    params = (new_link, brand_id)
    db.execute_query(query, params)
    logger.info(f"Ссылка марки обновлена: brand_id={brand_id}, new_link={new_link}")


def delete_brand(brand_id):
    """Удаление марки по её ID."""
    query = "DELETE FROM brands WHERE id = %s"
    params = (brand_id,)
    db.execute_query(query, params)
    logger.info(f"Марка удалена: brand_id={brand_id}")


def close_db_connection():
    """Закрытие соединения с базой данных."""
    db.close()
    logger.info("Соединение с БД закрыто в brand_crud")