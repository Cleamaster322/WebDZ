from db.database import Database
from utils.logger import setup_logger

db = Database()
logger = setup_logger(__name__)


def add_configuration(generation_id, configuration):
    """Добавление новой комплектации в таблицу configurations, если она ещё не существует."""
    name = configuration.get("name", "")
    link = configuration.get("link", "")
    date_start = configuration.get("date_start", "")
    date_end = configuration.get("date_end", "")
    engine_name = configuration.get("engine_name", "")

    if not link:
        logger.warning(
            "Нельзя сохранить комплектацию без ссылки: generation_id=%s, name=%s",
            generation_id,
            name,
        )
        return

    if configuration_exists(generation_id, link):
        logger.warning(
            "Комплектация уже существует: generation_id=%s, link=%s, name=%s",
            generation_id,
            link,
            name,
        )
        return

    query = """
        INSERT INTO configurations (
            generation_id,
            name,
            link,
            date_start,
            date_end,
            engine_name
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    params = (
        generation_id,
        name,
        link,
        date_start,
        date_end,
        engine_name,
    )

    try:
        db.execute_query(query, params)
        logger.info(
            "Комплектация успешно добавлена: generation_id=%s, name=%s, link=%s",
            generation_id,
            name,
            link,
        )
    except Exception as e:
        logger.error(
            "Ошибка при добавлении комплектации: generation_id=%s, name=%s, link=%s, error=%s",
            generation_id,
            name,
            link,
            e,
            exc_info=True,
        )

def configuration_exists(generation_id, link):
    """Проверка, существует ли комплектация для данного поколения по ссылке."""
    query = """
        SELECT id
        FROM configurations
        WHERE generation_id = %s
          AND link = %s
    """
    params = (generation_id, link)

    try:
        result = db.fetch_all(query, params)
        exists = len(result) > 0

        logger.debug(
            "Проверка существования комплектации: generation_id=%s, link=%s, exists=%s",
            generation_id,
            link,
            exists,
        )
        return exists
    except Exception as e:
        logger.error(
            "Ошибка при проверке существования комплектации: generation_id=%s, link=%s, error=%s",
            generation_id,
            link,
            e,
            exc_info=True,
        )
        raise

def get_configuration_by_name(generation_id, name):
    """Получение комплектации по имени и ID поколения."""
    query = """
        SELECT id, generation_id, name, link, date_start, date_end, engine_name
        FROM configurations
        WHERE generation_id = %s AND name = %s
    """
    params = (generation_id, name)

    try:
        result = db.fetch_all(query, params)
        config = result[0] if result else None

        logger.debug(
            "Получение комплектации по имени: generation_id=%s, name=%s, found=%s",
            generation_id,
            name,
            config is not None,
        )
        return config
    except Exception as e:
        logger.error(
            "Ошибка при получении комплектации по имени: generation_id=%s, name=%s, error=%s",
            generation_id,
            name,
            e,
            exc_info=True,
        )
        raise


def get_all_configurations():
    """Получение всех комплектаций."""
    query = """
        SELECT id, generation_id, name, link, date_start, date_end, engine_name
        FROM configurations
    """
    try:
        result = db.fetch_all(query)
        logger.info("Получены все комплектации: count=%s", len(result))
        return result
    except Exception as e:
        logger.error(
            "Ошибка при получении всех комплектаций: %s",
            e,
            exc_info=True,
        )
        raise


def get_all_configurations_by_generation(generation_id):
    """Получение всех комплектаций для данного поколения."""
    query = """
        SELECT id, generation_id, name, link, date_start, date_end, engine_name
        FROM configurations
        WHERE generation_id = %s
    """
    params = (generation_id,)

    try:
        result = db.fetch_all(query, params)
        logger.info(
            "Получены комплектации по поколению: generation_id=%s, count=%s",
            generation_id,
            len(result),
        )
        return result
    except Exception as e:
        logger.error(
            "Ошибка при получении комплектаций по поколению: generation_id=%s, error=%s",
            generation_id,
            e,
            exc_info=True,
        )
        raise


def delete_configuration(configuration_id):
    """Удаление комплектации по ID."""
    query = "DELETE FROM configurations WHERE id = %s"
    params = (configuration_id,)

    try:
        db.execute_query(query, params)
        logger.info("Комплектация успешно удалена: id=%s", configuration_id)
    except Exception as e:
        logger.error(
            "Ошибка при удалении комплектации: id=%s, error=%s",
            configuration_id,
            e,
            exc_info=True,
        )


def close_db_connection():
    """Закрытие соединения с базой данных."""
    try:
        db.close()
        logger.info("Соединение с БД закрыто для configuration_crud")
    except Exception as e:
        logger.error(
            "Ошибка при закрытии соединения с БД в configuration_crud: %s",
            e,
            exc_info=True,
        )
