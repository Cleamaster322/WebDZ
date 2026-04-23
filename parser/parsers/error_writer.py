import json
import os
from datetime import datetime


def _get_logs_dir() -> str:
    parser_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logs_dir = os.path.join(parser_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def _get_error_file_path() -> str:
    return os.path.join(_get_logs_dir(), "parser_errors.jsonl")


def write_parser_error(error_type: str, data: dict) -> None:
    """
    Записывает ошибку в parser/logs/parser_errors.jsonl
    Формат: одна JSON-строка = одна ошибка
    """
    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "error_type": error_type,
        "data": data,
    }

    file_path = _get_error_file_path()

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[ERROR_WRITER] Не удалось записать ошибку в файл: {e}")