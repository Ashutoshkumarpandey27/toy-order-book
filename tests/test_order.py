import pytest
from order import Order


def test_valid_buy_order():
    order = Order(1, "BUY", 100, 10)

    assert order.order_id == 1
    assert order.side == "BUY"
    assert order.price == 100
    assert order.quantity == 10


def test_valid_sell_order():
    order = Order(2, "SELL", 105, 5)

    assert order.side == "SELL"
    assert order.price == 105


def test_invalid_side():
    with pytest.raises(ValueError):
        Order(3, "INVALID", 100, 10)


def test_invalid_price():
    with pytest.raises(ValueError):
        Order(4, "BUY", -5, 10)


def test_zero_price():
    with pytest.raises(ValueError):
        Order(5, "BUY", 0, 10)


def test_invalid_quantity():
    with pytest.raises(ValueError):
        Order(6, "BUY", 100, -1)


def test_zero_quantity():
    with pytest.raises(ValueError):
        Order(7, "SELL", 100, 0)