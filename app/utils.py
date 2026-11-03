from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from app.exceptions import ValidationError


def parse_amount(text: str) -> int:
    """Превращает строку вроде '1 234,50' в копейки (int)."""
    cleaned = "".join(text.split()).replace(",", ".")
    if not cleaned:
        raise ValidationError("Введите сумму")

    try:
        value = Decimal(cleaned)
    except InvalidOperation:
        raise ValidationError("Сумма должна быть числом") from None

    if not value.is_finite():
        raise ValidationError("Сумма должна быть числом")
    if value <= 0:
        raise ValidationError("Сумма должна быть больше нуля")

    cents = value * 100
    if cents != cents.to_integral_value():
        raise ValidationError("Не больше двух знаков после запятой")
    return int(cents)

def parse_date(text: str) -> str:
    """Превращает 'ДД.ММ.ГГГГ' в 'ГГГГ-ММ-ДД'."""
    try:
        parsed = datetime.strptime(text.strip(), "%d.%m.%Y")
    except ValueError:
        raise ValidationError("Дата должна быть в правильном формате (ДД.ММ.ГГГГ)")from None
    return parsed.date().isoformat()

def format_date(iso: str) -> str:
    """Превращает 'ГГГГ-ММ-ДД' в 'ДД.ММ.ГГГГ'."""
    d = date.fromisoformat(iso)
    return d.strftime("%d.%m.%Y")

def today_iso() -> str:
    """Сегодняшняя дата в iso формате"""
    return date.today().isoformat()

def format_amount(cents: int) -> str:
    """Превращает копейки в строку для экрана: 123450 -> '1 234,50 руб.'"""
    rub, kop = divmod(cents, 100)
    rub_text = f"{rub:,}".replace(",", " ")
    return f"{rub_text},{kop:02d} руб."
