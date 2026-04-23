import re
from datetime import datetime

LOG_FILE = "logs/parser.log"
START_TIME = datetime.strptime("2026-04-23 10:28:04,552", "%Y-%m-%d %H:%M:%S,%f")

# Ошибка на уровне поколения
GENERATION_ERROR_RE = re.compile(
    r"Ошибка при разборе поколения для модели id=(?P<model_id>\d+), "
    r"name=(?P<model_name>.*?), region=(?P<region>.*?): (?P<error>.*)"
)

# Ошибка на уровне модели
MODEL_ERROR_RE = re.compile(
    r"Ошибка при обработке модели id=(?P<model_id>\d+), "
    r"name=(?P<model_name>.*?): (?P<error>.*)"
)

# Строка "Добавление поколения..." полезна, чтобы подтянуть generation/link, если ошибка сразу после неё
ADDING_GENERATION_RE = re.compile(
    r"Добавление поколения для модели id=(?P<model_id>\d+), "
    r"name=(?P<model_name>.*?), region=(?P<region>.*?): (?P<data>\{.*\})"
)

# Общий префикс времени лога
TIMESTAMP_RE = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \|")

def parse_ts(line: str):
    m = TIMESTAMP_RE.match(line)
    if not m:
        return None
    try:
        return datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S,%f")
    except ValueError:
        return None

def main():
    results = {}
    last_generation_context = {}

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            ts = parse_ts(line)
            if ts is None or ts < START_TIME:
                continue

            # Запоминаем последний контекст "Добавление поколения..."
            m_add = ADDING_GENERATION_RE.search(line)
            if m_add:
                model_id = int(m_add.group("model_id"))
                last_generation_context[model_id] = {
                    "region": m_add.group("region"),
                    "raw_generation_data": m_add.group("data"),
                }
                continue

            # Ошибка уровня поколения
            m_gen = GENERATION_ERROR_RE.search(line)
            if m_gen:
                model_id = int(m_gen.group("model_id"))
                model_name = m_gen.group("model_name")
                region = m_gen.group("region")
                error = m_gen.group("error")

                if model_id not in results:
                    results[model_id] = {
                        "model_name": model_name,
                        "errors": []
                    }

                results[model_id]["errors"].append({
                    "level": "generation",
                    "region": region,
                    "error": error,
                    "context": last_generation_context.get(model_id),
                    "log_line": line,
                })
                continue

            # Ошибка уровня модели
            m_model = MODEL_ERROR_RE.search(line)
            if m_model:
                model_id = int(m_model.group("model_id"))
                model_name = m_model.group("model_name")
                error = m_model.group("error")

                if model_id not in results:
                    results[model_id] = {
                        "model_name": model_name,
                        "errors": []
                    }

                results[model_id]["errors"].append({
                    "level": "model",
                    "region": None,
                    "error": error,
                    "context": None,
                    "log_line": line,
                })

    print(f"\nНайдено моделей с ошибками: {len(results)}\n")

    for model_id, info in results.items():
        print("=" * 100)
        print(f"MODEL ID: {model_id}")
        print(f"MODEL NAME: {info['model_name']}")
        print(f"ERROR COUNT: {len(info['errors'])}")
        for idx, err in enumerate(info["errors"], 1):
            print(f"\n  ERROR #{idx}")
            print(f"  LEVEL: {err['level']}")
            print(f"  REGION: {err['region']}")
            print(f"  ERROR: {err['error']}")
            if err["context"]:
                print(f"  CONTEXT: {err['context']}")
            print(f"  LOG: {err['log_line']}")
        print()

if __name__ == "__main__":
    main()