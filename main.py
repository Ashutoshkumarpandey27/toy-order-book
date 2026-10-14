
from order import Order
from order_book import OrderBook


# Test 1: Validate orders
print("\n--- Order Validation Test ---")

try:
    order1 = Order(1, "BUY", 100, 10)
    print("Valid order:", order1.price)

    order2 = Order(2, "SELL", -5, 10)
    print("Invalid order:", order2.price)

except ValueError as e:
    print("Order rejected:", e)

print("Program continues...")


# Test 2: Store BUY and SELL orders
print("\n--- Order Storage Test ---")

book = OrderBook()

order1 = Order(1, "BUY", 100, 5)
order2 = Order(2, "SELL", 105, 3)
order3 = Order(3, "BUY", 98, 2)
order4 = Order(4, "BUY", 110, 4)
order5 = Order(5, "SELL", 95, 6)
order6 = Order(6, "BUY", 100, 8)
order7 = Order(7, "BUY", 100, 5)
order8 = Order(8, "BUY", 100, 5)
order9 = Order(9, "BUY", 100, 5)

book.add_order(order1)
book.add_order(order2)
book.add_order(order3)
book.add_order(order4)
book.add_order(order5)
book.add_order(order6)
book.add_order(order7)
book.add_order(order8)
book.add_order(order9)

print("BUY orders:", len(book.buy_orders))
print("SELL orders:", len(book.sell_orders))


# Test 3: Sort orders
print("\n--- Sorting Test ---")

book.sort_buy_orders()
book.sort_sell_orders()

book.display_orders()


# Test 4: Match orders
print("\n--- Matching Test ---")

test_book = OrderBook()

test_buy = Order(101, "BUY", 200, 10)
test_sell = Order(102, "SELL", 190, 6)

test_book.add_order(test_buy)
test_book.add_order(test_sell)

test_book.match_orders()
test_book.display_orders()


# Test 5: Cancel orders
print("\n--- Cancellation Test ---")

cancel_book = OrderBook()

cancel_book.add_order(Order(201, "BUY", 100, 5))
cancel_book.add_order(Order(202, "SELL", 105, 3))
cancel_book.add_order(Order(203, "BUY", 98, 2))

print("\nBefore cancellation:")
cancel_book.display_orders()

# Cancel an existing BUY order
cancel_book.cancel_order(201)

print("\nAfter cancelling order 201:")
cancel_book.display_orders()

# Cancel an existing SELL order
cancel_book.cancel_order(202)

print("\nAfter cancelling order 202:")
cancel_book.display_orders()

# Try cancelling a nonexistent order
cancel_book.cancel_order(999)

print("\n--- All Tests Completed ---")


print("\n--- Price-Time Priority Test ---")

book = OrderBook()

# Same price: Order 301 arrives first
book.add_order(Order(301, "BUY", 100, 5))
book.add_order(Order(302, "BUY", 100, 8))

# SELL order matches both BUY orders
book.add_order(Order(303, "SELL", 100, 6))

book.match_orders()

print("\nRemaining orders:")
book.display_orders()
