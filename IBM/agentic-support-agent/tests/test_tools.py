import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.order_lookup import order_lookup
from tools.calculator import calculator
from tools.weather import get_weather


def test_order_lookup_found():
    result = order_lookup("1025")
    assert result["found"] is True
    assert result["status"] == "Shipped"
    assert result["subtotal"] == 799.0 + 2 * 299.0


def test_order_lookup_not_found():
    result = order_lookup("9999")
    assert result["found"] is False


def test_calculator_basic():
    result = calculator("2 + 2 * 3")
    assert result["result"] == 8


def test_calculator_rejects_unsafe_input():
    result = calculator("__import__('os').system('echo hi')")
    assert "error" in result


def test_weather_deterministic_per_city():
    a = get_weather("Chennai")
    b = get_weather("Chennai")
    assert a == b
    assert "temperature_c" in a
