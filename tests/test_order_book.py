
import pytest
from order import Order
from order_book import OrderBook


def test_partial_matching():
    book = OrderBook()

    buy = Order(1, "BUY", 100, 10)
    sell = Order(2, "SELL", 100, 6)

    book.add_order(buy)
    book.add_order(sell)
    book.match_orders()

    assert len(book.buy_orders) == 1
    assert book.buy_orders[0].quantity == 4
    assert len(book.sell_orders) == 0


def test_fully_filled_orders_are_removed():
    book = OrderBook()

    book.add_order(Order(1, "BUY", 100, 5))
    book.add_order(Order(2, "SELL", 100, 5))

    book.match_orders()

    assert len(book.buy_orders) == 0
    assert len(book.sell_orders) == 0


def test_price_time_priority():
    book = OrderBook()

    first_buy = Order(301, "BUY", 100, 5)
    second_buy = Order(302, "BUY", 100, 8)
    sell = Order(303, "SELL", 100, 6)

    book.add_order(first_buy)
    book.add_order(second_buy)
    book.add_order(sell)

    book.match_orders()

    assert first_buy.quantity == 0
    assert second_buy.quantity == 7
    assert len(book.buy_orders) == 1
    assert book.buy_orders[0].order_id == 302
    assert len(book.sell_orders) == 0


def test_highest_buy_price_gets_priority():
    book = OrderBook()

    lower_buy = Order(1, "BUY", 100, 5)
    higher_buy = Order(2, "BUY", 110, 5)
    sell = Order(3, "SELL", 105, 5)

    book.add_order(lower_buy)
    book.add_order(higher_buy)
    book.add_order(sell)

    book.match_orders()

    assert higher_buy.quantity == 0
    assert lower_buy.quantity == 5
    assert len(book.buy_orders) == 1
    assert book.buy_orders[0].order_id == 1


def test_lowest_sell_price_gets_priority():
    book = OrderBook()

    buy = Order(1, "BUY", 110, 5)
    higher_sell = Order(2, "SELL", 105, 5)
    lower_sell = Order(3, "SELL", 100, 5)

    book.add_order(buy)
    book.add_order(higher_sell)
    book.add_order(lower_sell)

    book.match_orders()

    assert lower_sell.quantity == 0
    assert higher_sell.quantity == 5
    assert len(book.sell_orders) == 1
    assert book.sell_orders[0].order_id == 2


def test_non_matching_orders_remain_in_book():
    book = OrderBook()

    buy = Order(1, "BUY", 100, 5)
    sell = Order(2, "SELL", 105, 5)

    book.add_order(buy)
    book.add_order(sell)
    book.match_orders()

    assert len(book.buy_orders) == 1
    assert len(book.sell_orders) == 1
    assert buy.quantity == 5
    assert sell.quantity == 5


def test_cancel_buy_order():
    book = OrderBook()
    book.add_order(Order(1, "BUY", 100, 5))

    book.cancel_order(1)

    assert len(book.buy_orders) == 0


def test_cancel_sell_order():
    book = OrderBook()
    book.add_order(Order(2, "SELL", 105, 5))

    book.cancel_order(2)

    assert len(book.sell_orders) == 0


def test_matching_with_empty_book():
    book = OrderBook()

    book.match_orders()

    assert len(book.buy_orders) == 0
    assert len(book.sell_orders) == 0



def test_duplicate_order_id_is_rejected():
    book = OrderBook()

    book.add_order(Order(1, "BUY", 100, 5))

    duplicate = Order(1, "SELL", 105, 3)

    import pytest

    with pytest.raises(ValueError, match="Duplicate order ID"):
        book.add_order(duplicate)

    assert len(book.buy_orders) == 1
    assert len(book.sell_orders) == 0


def test_trade_history_is_recorded():
    book = OrderBook()

    book.add_order(Order(101, "BUY", 200, 10))
    book.add_order(Order(102, "SELL", 190, 6))

    book.match_orders()

    assert len(book.trades) == 1

    assert book.trades[0] == {
        "buy_order_id": 101,
        "sell_order_id": 102,
        "price": 190,
        "quantity": 6
    }


def test_no_trade_history_when_orders_do_not_match():
    book = OrderBook()

    book.add_order(Order(201, "BUY", 100, 5))
    book.add_order(Order(202, "SELL", 110, 5))

    book.match_orders()

    assert book.trades == []
