import logging
import os

def setup_logger(name="parser"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "parser.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # чтобы не дублировались хендлеры
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # файл
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # консоль (оставим, но можно убрать позже)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger