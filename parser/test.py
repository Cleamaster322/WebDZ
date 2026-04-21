from db.database import Database

# Создаём объект класса Database для работы с БД
db = Database()

def add_configuration(generation_id, configuration):
    """Добавление новой комплектации в таблицу configurations, если она ещё не существует."""
    if not configuration_exists(generation_id, configuration['name']):
        query = """
            INSERT INTO configurations (
                generation_id, name, link, date_start, date_end, engine_name
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            generation_id,
            configuration['name'],
            configuration['link'],
            configuration['date_start'],
            configuration['date_end'],
            configuration['engine_name']
        )
        try:
            db.execute_query(query, params)
            db.connection.commit() # исправил
            print(f"✅ Комплектация {configuration['name']} успешно добавлена для поколения с ID {generation_id}")
        except Exception as e:
            print(f"⚠️ Ошибка при добавлении комплектации {configuration['name']}: {e}")
    else:
        print(f"⚠️ Комплектация {configuration['name']} уже существует для поколения с ID {generation_id}")


def configuration_exists(generation_id, name):
    """Проверка, существует ли комплектация с таким именем для данного поколения."""
    query = """
        SELECT COUNT(*) FROM configurations
        WHERE generation_id = %s AND name = %s
    """
    params = (generation_id, name)
    result = db.fetch_one(query, params)
    return result['COUNT(*)'] > 0 if result else False # исправил


def get_configuration_by_name(generation_id, name):
    """Получение комплектации по имени и ID поколения."""
    query = """
        SELECT id, generation_id, name, link, date_start, date_end, engine_name
        FROM configurations
        WHERE generation_id = %s AND name = %s
    """
    params = (generation_id, name)
    result = db.fetch_one(query, params)
    return result


def get_all_configurations_by_generation(generation_id):
    """Получение всех комплектаций для данного поколения."""
    query = """
        SELECT id, generation_id, name, link, date_start, date_end, engine_name
        FROM configurations
        WHERE generation_id = %s
    """
    params = (generation_id,)
    return db.fetch_all(query, params)

def delete_configuration(configuration_id):
    """Удаление комплектации по ID."""
    query = "DELETE FROM configurations WHERE id = %s"
    params = (configuration_id,)
    try:
        db.execute_query(query, params)
        db.connection.commit() # исправил
        print(f"✅ Комплектация с ID {configuration_id} успешно удалена.")
    except Exception as e:
        print(f"⚠️ Ошибка при удалении комплектации с ID {configuration_id}: {e}")

def close_db_connection():
    """Закрытие соединения с базой данных."""
    db.close()