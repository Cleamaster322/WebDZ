import json
from datetime import datetime

FILE_PATH = "logs/parser_errors.jsonl"

# ВАЖНО: формат с миллисекундами
START_TIME = datetime.strptime("2026-04-23 10:28:04,552", "%Y-%m-%d %H:%M:%S,%f")


def parse_time(ts: str):
    """
    Парсим timestamp вида:
    2026-04-23 10:28:04,552
    """
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S,%f")
    except:
        return None


def main():
    results = {}

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
            except:
                continue

            ts = parse_time(record.get("timestamp", ""))
            if not ts or ts < START_TIME:
                continue

            data = record.get("data", {})

            model_id = data.get("model_id")
            if not model_id:
                continue

            if model_id not in results:
                results[model_id] = {
                    "model_name": data.get("model_name"),
                    "model_link": data.get("model_link"),
                    "brand_id": data.get("brand_id"),
                    "errors": []
                }

            results[model_id]["errors"].append({
                "time": record.get("timestamp"),
                "type": record.get("error_type"),
                "error": data.get("error"),
                "generation_name": data.get("generation_name"),
                "generation_link": data.get("generation_link"),
                "region": data.get("region"),
            })

    # Вывод
    print(f"\nНайдено моделей с ошибками: {len(results)}\n")

    for model_id, info in results.items():
        print("=" * 80)
        print(f"MODEL ID: {model_id}")
        print(f"NAME: {info['model_name']}")
        print(f"LINK: {info['model_link']}")
        print(f"ERROR COUNT: {len(info['errors'])}")

        for err in info["errors"]:
            print("  -", err)

        print()


if __name__ == "__main__":
    main()