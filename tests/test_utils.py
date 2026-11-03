import pytest

from app.exceptions import ValidationError
from app.utils import parse_amount, parse_date, format_amount, format_date

@pytest.mark.parametrize("text, expected", [
    ("1234", 123400),
    ("1 234,50", 123450),
    ("99.9", 9990),
    ("0,01", 1),
])
def test_parse_amount_valid(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize("text", ["", "   ", "abc", "0", "-5", "1,2,3"])
def test_parse_amount_invalid(text):
    with pytest.raises(ValidationError):
        parse_amount(text)

@pytest.mark.parametrize("text, expected", [
    ("02.11.2026", "2026-11-02"),
    ("29.02.2028", "2028-02-29"),
])
def test_parse_date_valid(text, expected):
    assert parse_date(text) == expected


@pytest.mark.parametrize("text", ["31.02.2026", "2026-11-02", "", "2.11"])
def test_parse_date_invalid(text):
    with pytest.raises(ValidationError):
        parse_date(text)


@pytest.mark.parametrize("cents, expected", [
    (123450, "1 234,50 руб."),
    (5, "0,05 руб."),
    (100, "1,00 руб."),
])
def test_format_amount(cents, expected):
    assert format_amount(cents) == expected


def test_format_date():
    assert format_date("2026-11-02") == "02.11.2026"
