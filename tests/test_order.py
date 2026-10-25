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




import pytest
from order import Order


@pytest.mark.parametrize(
    "price",
    [float("nan"), float("inf"), -float("inf")]
)
def test_limit_order_rejects_non_finite_price(price):
    with pytest.raises(ValueError):
        Order(201, "BUY", price, 5)


@pytest.mark.parametrize(
    "quantity",
    [float("nan"), float("inf"), -float("inf")]
)
def test_order_rejects_non_finite_quantity(quantity):
    with pytest.raises(ValueError):
        Order(202, "BUY", 100, quantity)


@pytest.mark.parametrize("price", ["abc", None, True])
def test_order_rejects_invalid_price_type(price):
    with pytest.raises(ValueError):
        Order(203, "BUY", price, 5)


@pytest.mark.parametrize("quantity", ["abc", None, True])
def test_order_rejects_invalid_quantity_type(quantity):
    with pytest.raises(ValueError):
        Order(204, "BUY", 100, quantity)
