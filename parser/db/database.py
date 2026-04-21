import mysql.connector
from mysql.connector import Error
from config.settings import SettingsDB
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Database:
    def __init__(self):
        """Инициализация базы данных с настройками подключения."""
        self.host = SettingsDB.DB_HOST
        self.user = SettingsDB.DB_USER
        self.password = SettingsDB.DB_PASSWORD
        self.database = SettingsDB.DB_NAME
        self.connection = None
        self.connect()

    def connect(self):
        """Подключение к базе данных MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                logger.info("Успешное подключение к MySQL")
        except Error as e:
            logger.error(f"Ошибка подключения к MySQL: {e}", exc_info=True)
            self.connection = None

    def ensure_connection(self):
        """Проверка и восстановление соединения с БД."""
        if self.connection is None or not self.connection.is_connected():
            logger.warning("Соединение с БД потеряно. Переподключение...")
            self.connect()

        if self.connection is None or not self.connection.is_connected():
            logger.error("Не удалось восстановить соединение с MySQL")
            raise ConnectionError("Не удалось установить соединение с MySQL")

    def execute_query(self, query, params=None):
        cursor = None
        try:
            self.ensure_connection()

            logger.debug(f"SQL EXECUTE: {query} | params={params}")

            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()

            logger.debug("Запрос выполнен успешно")

        except (Error, ConnectionError) as e:
            logger.error(
                f"Ошибка выполнения запроса: {query} | {e}",
                exc_info=True
            )
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=None):
        cursor = None
        try:
            self.ensure_connection()

            logger.debug(f"SQL FETCH: {query} | params={params}")

            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()

            logger.debug(f"Получено строк: {len(result)}")

            return result

        except (Error, ConnectionError) as e:
            logger.error(
                f"Ошибка получения данных: {query} | {e}",
                exc_info=True
            )
            return []

        finally:
            if cursor:
                cursor.close()

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Соединение с MySQL закрыто")