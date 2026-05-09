from db.database import Database
from utils.logger import setup_logger

db = Database()
logger = setup_logger(__name__)


def add_car(configuration_id, car_data):
    """Добавление записи car_data для комплектации, если она ещё не существует."""
    logger.info(f"Попытка добавить car_data для configuration_id={configuration_id}")
    logger.info(f"DEBUG car_crud file path: {__file__}")
    if car_exists(configuration_id):
        logger.info(
            f"car_data уже существует для configuration_id={configuration_id}, выполняем обновление"
        )
        return update_car(configuration_id, car_data)

    query = """
        INSERT INTO car_data (
            configuration_id,
            configuration_name,
            manufacture_year,
            front_tires,
            rear_tires,
            fuel_type,
            transmission,
            drive_type,
            seats_count,
            clearance,
            body_type,
            body_mark,
            vehicle_weight_kg,
            engine_model,
            engine_power_hp,
            engine_power_kw,
            cylinder_layout,
            cylinders_count,
            turbo_present,
            front_brakes,
            rear_brakes,
            vehicle_length_mm,
            vehicle_width_mm,
            vehicle_height_mm
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        configuration_id,
        car_data.get("configuration_name"),
        car_data.get("manufacture_year"),
        car_data.get("front_tires"),
        car_data.get("rear_tires"),
        car_data.get("fuel_type"),
        car_data.get("transmission"),
        car_data.get("drive_type"),
        car_data.get("seats_count"),
        car_data.get("clearance_mm"),
        car_data.get("body_type"),
        car_data.get("body_mark"),
        car_data.get("vehicle_weight_kg"),
        car_data.get("engine_model"),
        car_data.get("engine_power_hp"),
        car_data.get("engine_power_kw"),
        car_data.get("cylinder_layout"),
        car_data.get("cylinders_count"),
        car_data.get("turbo_present"),
        car_data.get("front_brakes"),
        car_data.get("rear_brakes"),
        car_data.get("vehicle_length_mm"),
        car_data.get("vehicle_width_mm"),
        car_data.get("vehicle_height_mm"),
    )

    try:
        db.execute_query(query, params)
        logger.info(
            f"car_data успешно добавлена для configuration_id={configuration_id}"
        )
        return True
    except Exception as e:
        logger.error(
            f"Ошибка при добавлении car_data для configuration_id={configuration_id}: {e}",
            exc_info=True,
        )
        return False


def update_car(configuration_id, car_data):
    """Обновление car_data для существующей комплектации."""
    query = """
        UPDATE car_data
        SET
            configuration_name = %s,
            manufacture_year = %s,
            front_tires = %s,
            rear_tires = %s,
            fuel_type = %s,
            transmission = %s,
            drive_type = %s,
            seats_count = %s,
            clearance = %s,
            body_type = %s,
            body_mark = %s,
            vehicle_weight_kg = %s,
            engine_model = %s,
            engine_power_hp = %s,
            engine_power_kw = %s,
            cylinder_layout = %s,
            cylinders_count = %s,
            turbo_present = %s,
            front_brakes = %s,
            rear_brakes = %s,
            vehicle_length_mm = %s,
            vehicle_width_mm = %s,
            vehicle_height_mm = %s
        WHERE configuration_id = %s
    """

    params = (
        car_data.get("configuration_name"),
        car_data.get("manufacture_year"),
        car_data.get("front_tires"),
        car_data.get("rear_tires"),
        car_data.get("fuel_type"),
        car_data.get("transmission"),
        car_data.get("drive_type"),
        car_data.get("seats_count"),
        car_data.get("clearance_mm"),
        car_data.get("body_type"),
        car_data.get("body_mark"),
        car_data.get("vehicle_weight_kg"),
        car_data.get("engine_model"),
        car_data.get("engine_power_hp"),
        car_data.get("engine_power_kw"),
        car_data.get("cylinder_layout"),
        car_data.get("cylinders_count"),
        car_data.get("turbo_present"),
        car_data.get("front_brakes"),
        car_data.get("rear_brakes"),
        car_data.get("vehicle_length_mm"),
        car_data.get("vehicle_width_mm"),
        car_data.get("vehicle_height_mm"),
        configuration_id,
    )

    try:
        logger.info(
            f"DEBUG POWER update_car configuration_id={configuration_id}: "
            f"hp={car_data.get('engine_power_hp')}, "
            f"kw={car_data.get('engine_power_kw')}, "
            f"keys={list(car_data.keys())}"
        )
        db.execute_query(query, params)
        logger.info(f"car_data успешно обновлена для configuration_id={configuration_id}")
        return True
    except Exception as e:
        logger.error(
            f"Ошибка при обновлении car_data для configuration_id={configuration_id}: {e}",
            exc_info=True,
        )
        return False


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
        SELECT
            id,
            configuration_id,
            configuration_name,
            manufacture_year,
            front_tires,
            rear_tires,
            fuel_type,
            transmission,
            drive_type,
            seats_count,
            clearance,
            body_type,
            body_mark,
            vehicle_weight_kg,
            engine_model,
            engine_power_hp,
            engine_power_kw,
            cylinder_layout,
            cylinders_count,
            turbo_present,
            front_brakes,
            rear_brakes,
            vehicle_length_mm,
            vehicle_width_mm,
            vehicle_height_mm
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
    """Удаление car_data по ID."""
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

def get_configurations_with_missing_power():
    query = """
        SELECT
            c.id,
            c.generation_id,
            c.name,
            c.link,
            c.engine_name,
            c.date_start,
            c.date_end
        FROM configurations c
        INNER JOIN car_data cd ON cd.configuration_id = c.id
        WHERE cd.engine_power_hp IS NULL
           OR cd.engine_power_kw IS NULL
        ORDER BY c.id
    """

    try:
        result = db.fetch_all(query)
        logger.info(
            f"Получены комплектации с пустой мощностью: count={len(result)}"
        )
        return result
    except Exception as e:
        logger.error(
            f"Ошибка при получении комплектаций с пустой мощностью: {e}",
            exc_info=True,
        )
        return []

def close_db_connection():
    """Закрытие соединения с базой данных."""
    logger.info("Закрытие соединения с БД в car_crud")
    db.close()