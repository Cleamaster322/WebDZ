from decimal import Decimal, InvalidOperation


def is_empty(value):
    return value is None or value == ""


def decimal_value(value):
    if is_empty(value):
        return None

    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def fmt_text(value, default=""):
    if is_empty(value):
        return default
    return str(value)


def fmt_num(value, digits=1, default=""):
    number = decimal_value(value)

    if number is None:
        return default

    quant = Decimal("1") if digits == 0 else Decimal("1." + ("0" * digits))
    number = number.quantize(quant)

    return str(number).replace(".", ",")


def fmt_int(value, default=""):
    number = decimal_value(value)

    if number is None:
        return default

    return str(int(number))


def fmt_bool(value, true_label="Да", false_label="Нет", default=""):
    if value is True:
        return true_label
    if value is False:
        return false_label
    return default


def fmt_date(value, default=""):
    if not value:
        return default

    return value.strftime("%d.%m.%Y")


def safe_div(numerator, denominator):
    numerator = decimal_value(numerator)
    denominator = decimal_value(denominator)

    if numerator is None or denominator is None or denominator == 0:
        return None

    return numerator / denominator