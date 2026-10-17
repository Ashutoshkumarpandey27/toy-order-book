
from order import Order
from order_book import OrderBook


# Test 1: Order Validation
print("\n--- Order Validation Test ---")

try:
    valid_order = Order(1, "BUY", 100, 10)
    print("Valid order created:", valid_order.price)

    invalid_order = Order(2, "SELL", -5, 10)
    print("Invalid order:", invalid_order.price)

except ValueError as e:
    print("Order rejected:", e)

print("Program continues...")


# Test 2: Order Storage
print("\n--- Order Storage Test ---")

book = OrderBook()

orders = [
    Order(1, "BUY", 100, 5),
    Order(2, "SELL", 105, 3),
    Order(3, "BUY", 98, 2),
    Order(4, "BUY", 110, 4),
    Order(5, "SELL", 95, 6),
    Order(6, "BUY", 100, 8),
    Order(7, "BUY", 100, 5),
    Order(8, "BUY", 100, 5),
    Order(9, "BUY", 100, 5),
]

for order in orders:
    book.add_order(order)

print("BUY orders:", len(book.buy_orders))
print("SELL orders:", len(book.sell_orders))


# Test 3: Sorting
print("\n--- Sorting Test ---")

book.sort_buy_orders()
book.sort_sell_orders()
book.display_orders()


# Test 4: Matching
print("\n--- Matching Test ---")

test_book = OrderBook()

test_book.add_order(Order(101, "BUY", 200, 10))
test_book.add_order(Order(102, "SELL", 190, 6))

test_book.match_orders()
test_book.display_trades()

test_book.display_orders()


# Test 5: Cancellation
print("\n--- Cancellation Test ---")

cancel_book = OrderBook()

cancel_book.add_order(Order(201, "BUY", 100, 5))
cancel_book.add_order(Order(202, "SELL", 105, 3))
cancel_book.add_order(Order(203, "BUY", 98, 2))

print("\nBefore cancellation:")
cancel_book.display_orders()

cancel_book.cancel_order(201)

print("\nAfter cancelling order 201:")
cancel_book.display_orders()

cancel_book.cancel_order(202)

print("\nAfter cancelling order 202:")
cancel_book.display_orders()

cancel_book.cancel_order(999)


# Test 6: Price-Time Priority
print("\n--- Price-Time Priority Test ---")

priority_book = OrderBook()

# Same price: order 301 arrives first
priority_book.add_order(Order(301, "BUY", 100, 5))
priority_book.add_order(Order(302, "BUY", 100, 8))

# SELL order needs 6 units
priority_book.add_order(Order(303, "SELL", 100, 6))

priority_book.match_orders()

print("\nExpected remaining BUY order:")
print("Order 302 should have quantity 7.")

print("\nActual remaining orders:")
priority_book.display_orders()


print("\n--- All Tests Completed ---")
