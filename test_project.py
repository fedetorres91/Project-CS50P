import pytest
from project import format_currency, validate_password, format_date, main


def test_format_currency_default_symbol():
    assert format_currency(1234.56) == "$1,234.56"


def test_format_currency_zero():
    assert format_currency(0) == "$0.00"


def test_format_currency_custom_symbol():
    assert format_currency(50.0, "€") == "€50.00"


def test_validate_password_valid():
    assert validate_password("secret12") is True


def test_validate_password_exactly_min_length():
    assert validate_password("12345678") is True


def test_validate_password_too_short():
    with pytest.raises(ValueError):
        validate_password("short")


def test_validate_password_not_string():
    with pytest.raises(ValueError):
        validate_password(12345678)


def test_validate_password_custom_min_length():
    with pytest.raises(ValueError):
        validate_password("secret12", min_length=12)


def test_format_date_basic():
    assert format_date("2024-01-15T10:30:00") == "01/15/2024"


def test_format_date_with_microseconds():
    assert format_date("2024-12-31T23:59:59.999999") == "12/31/2024"


def test_main_is_callable():
    assert callable(main)
