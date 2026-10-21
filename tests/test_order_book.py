
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




def test_get_best_bid():
    book = OrderBook()

    book.add_order(Order(401, "BUY", 100, 5))
    book.add_order(Order(402, "BUY", 110, 3))
    book.add_order(Order(403, "BUY", 105, 7))

    assert book.get_best_bid() == 110


def test_get_best_bid_when_book_is_empty():
    book = OrderBook()

    assert book.get_best_bid() is None
def test_get_best_ask():
    book = OrderBook()

    book.add_order(Order(501, "SELL", 120, 5))
    book.add_order(Order(502, "SELL", 115, 3))
    book.add_order(Order(503, "SELL", 125, 7))

    assert book.get_best_ask() == 115


def test_get_best_ask_when_book_is_empty():
    book = OrderBook()

    assert book.get_best_ask() is None
def test_get_spread():
    book = OrderBook()

    book.add_order(Order(601, "BUY", 110, 5))
    book.add_order(Order(602, "SELL", 115, 3))

    assert book.get_spread() == 5


def test_get_spread_when_book_is_empty():
    book = OrderBook()

    assert book.get_spread() is None


def test_get_spread_when_one_side_is_empty():
    book = OrderBook()

    book.add_order(Order(603, "BUY", 110, 5))

    assert book.get_spread() is None 


def test_total_traded_volume():
    book = OrderBook()

    book.add_order(Order(701, "BUY", 110, 5))
    book.add_order(Order(702, "SELL", 100, 3))
    book.match_orders()

    book.add_order(Order(703, "BUY", 120, 4))
    book.add_order(Order(704, "SELL", 115, 2))
    book.match_orders()

    assert book.get_total_traded_volume() == 5


def test_total_traded_volume_when_no_trades():
    book = OrderBook()

    assert book.get_total_traded_volume() == 0


def test_total_traded_volume_with_partial_fill():
    book = OrderBook()

    book.add_order(Order(705, "BUY", 120, 10))
    book.add_order(Order(706, "SELL", 110, 4))
    book.match_orders()

    assert book.get_total_traded_volume() == 4



def test_market_depth_groups_buy_orders_by_price():
    book = OrderBook()

    book.add_order(Order(801, "BUY", 110, 5))
    book.add_order(Order(802, "BUY", 110, 3))
    book.add_order(Order(803, "BUY", 105, 7))

    depth = book.get_market_depth()

    assert depth["BUY"] == {
        110: 8,
        105: 7
    }


def test_market_depth_groups_sell_orders_by_price():
    book = OrderBook()

    book.add_order(Order(804, "SELL", 120, 4))
    book.add_order(Order(805, "SELL", 115, 6))
    book.add_order(Order(806, "SELL", 120, 2))

    depth = book.get_market_depth()

    assert depth["SELL"] == {
        115: 6,
        120: 6
    }


def test_market_depth_sorts_prices_correctly():
    book = OrderBook()

    book.add_order(Order(807, "BUY", 100, 2))
    book.add_order(Order(808, "BUY", 110, 3))
    book.add_order(Order(809, "SELL", 130, 4))
    book.add_order(Order(810, "SELL", 120, 5))

    depth = book.get_market_depth()

    assert list(depth["BUY"].keys()) == [110, 100]
    assert list(depth["SELL"].keys()) == [120, 130]


def test_market_depth_when_order_book_is_empty():
    book = OrderBook()

    assert book.get_market_depth() == {
        "BUY": {},
        "SELL": {}
    }

def test_cumulative_buy_market_depth():
    book = OrderBook()

    book.add_order(Order(901, "BUY", 110, 5))
    book.add_order(Order(902, "BUY", 110, 3))
    book.add_order(Order(903, "BUY", 105, 7))

    depth = book.get_cumulative_market_depth()

    assert depth["BUY"] == {
        110: 8,
        105: 15
    }


def test_cumulative_sell_market_depth():
    book = OrderBook()

    book.add_order(Order(904, "SELL", 115, 4))
    book.add_order(Order(905, "SELL", 120, 6))
    book.add_order(Order(906, "SELL", 120, 2))

    depth = book.get_cumulative_market_depth()

    assert depth["SELL"] == {
        115: 4,
        120: 12
    }


def test_cumulative_market_depth_when_empty():
    book = OrderBook()

    assert book.get_cumulative_market_depth() == {
        "BUY": {},
        "SELL": {}
    }


def test_cumulative_market_depth_keeps_price_order():
    book = OrderBook()

    book.add_order(Order(907, "BUY", 100, 2))
    book.add_order(Order(908, "BUY", 110, 3))
    book.add_order(Order(909, "SELL", 130, 4))
    book.add_order(Order(910, "SELL", 120, 5))

    depth = book.get_cumulative_market_depth()

    assert list(depth["BUY"].keys()) == [110, 100]
    assert list(depth["SELL"].keys()) == [120, 130]



def test_order_book_stats():
    book = OrderBook()

    book.add_order(Order(1001, "BUY", 100, 5))
    book.add_order(Order(1002, "BUY", 105, 3))
    book.add_order(Order(1003, "SELL", 110, 4))

    stats = book.get_order_book_stats()

    assert stats == {
        "active_buy_orders": 2,
        "active_sell_orders": 1,
        "total_buy_quantity": 8,
        "total_sell_quantity": 4,
        "total_active_orders": 3
    }


def test_order_book_stats_when_empty():
    book = OrderBook()

    assert book.get_order_book_stats() == {
        "active_buy_orders": 0,
        "active_sell_orders": 0,
        "total_buy_quantity": 0,
        "total_sell_quantity": 0,
        "total_active_orders": 0
    }

    
def test_vwap_with_multiple_trades():
    book = OrderBook()

    book.trades = [
        {
            "buy_order_id": 1,
            "sell_order_id": 2,
            "price": 50,
            "quantity": 2
        },
        {
            "buy_order_id": 3,
            "sell_order_id": 4,
            "price": 60,
            "quantity": 3
        }
    ]

    assert book.get_vwap() == pytest.approx(56.0)


def test_vwap_with_no_trades():
    book = OrderBook()

    assert book.get_vwap() is None


def test_vwap_with_single_trade():
    book = OrderBook()

    book.trades = [
        {
            "buy_order_id": 5,
            "sell_order_id": 6,
            "price": 100,
            "quantity": 4
        }
    ]

    assert book.get_vwap() == pytest.approx(100.0)



def test_vwap_after_actual_order_matching():
    book = OrderBook()

    book.add_order(Order(1101, "BUY", 110, 5))
    book.add_order(Order(1102, "SELL", 100, 3))

    book.match_orders()

    assert book.get_total_traded_volume() == 3
    assert book.get_vwap() == pytest.approx(100.0)

    # BUY order should have 2 units remaining
    assert len(book.buy_orders) == 1
    assert book.buy_orders[0].quantity == 2

    # SELL order should be completely filled
    assert len(book.sell_orders) == 0


