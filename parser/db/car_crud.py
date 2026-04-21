from db.database import Database
from utils.logger import setup_logger

db = Database()
logger = setup_logger(__name__)


def add_car(configuration_id, car_data):
    """Добавление записи car_data для комплектации, если она ещё не существует."""
    logger.info(f"Попытка добавить car_data для configuration_id={configuration_id}")

    if car_exists(configuration_id):
        logger.warning(
            f"car_data уже существует для configuration_id={configuration_id}"
        )
        return

    query = """
        INSERT INTO car_data (
            configuration_id,
            front_tires,
            rear_tires,
            engine_capacity,
            engine_power_hp,
            engine_power_kw,
            consumption,
            fuel_type,
            transmission,
            drive_type,
            seats_count,
            doors_count,
            clearance,
            trunk_volume
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        configuration_id,
        car_data.get("front_tires"),
        car_data.get("rear_tires"),
        car_data.get("engine_capacity"),
        car_data.get("engine_power_hp"),
        car_data.get("engine_power_kw"),
        car_data.get("consumption"),
        car_data.get("fuel_type"),
        car_data.get("transmission"),
        car_data.get("drive_type"),
        car_data.get("seats"),
        car_data.get("doors"),
        car_data.get("clearance"),
        car_data.get("trunk_volume"),
    )

    try:
        db.execute_query(query, params)
        logger.info(
            f"car_data успешно добавлена для configuration_id={configuration_id}"
        )
    except Exception as e:
        logger.error(
            f"Ошибка при добавлении car_data для configuration_id={configuration_id}: {e}",
            exc_info=True,
        )


def car_exists(configuration_id):
    """Проверка, существует ли запись car_data для данной комплектации."""
    query = """
        SELECT id
        FROM car_data
        WHERE configuration_id = %s
    """
    params = (configuration_id,)

    try:
        result = db.fetch_all(query, params)
        exists = len(result) > 0
        logger.info(
            f"Проверка существования car_data для configuration_id={configuration_id}: {exists}"
        )
        return exists
    except Exception as e:
        logger.error(
            f"Ошибка при проверке car_data для configuration_id={configuration_id}: {e}",
            exc_info=True,
        )
        return False


def get_cars_by_configuration(configuration_id):
    """Получение car_data по ID комплектации."""
    query = """
        SELECT id, configuration_id, front_tires, rear_tires, engine_capacity,
               engine_power_hp, engine_power_kw, consumption, fuel_type,
               transmission, drive_type, seats_count, doors_count,
               clearance, trunk_volume
        FROM car_data
        WHERE configuration_id = %s
    """
    params = (configuration_id,)

    try:
        result = db.fetch_all(query, params)
        logger.info(
            f"Получено записей car_data для configuration_id={configuration_id}: {len(result)}"
        )
        return result
    except Exception as e:
        logger.error(
            f"Ошибка при получении car_data для configuration_id={configuration_id}: {e}",
            exc_info=True,
        )
        return []


def delete_car(car_id):
    """Удаление машины по ID."""
    query = "DELETE FROM car_data WHERE id = %s"
    params = (car_id,)

    try:
        db.execute_query(query, params)
        logger.info(f"car_data с id={car_id} успешно удалена")
    except Exception as e:
        logger.error(
            f"Ошибка при удалении car_data с id={car_id}: {e}",
            exc_info=True,
        )


def close_db_connection():
    """Закрытие соединения с базой данных."""
    logger.info("Закрытие соединения с БД в car_crud")
    db.close()