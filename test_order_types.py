from order import Order

limit_order = Order(1, "BUY", 100, 5)
market_order = Order(2, "BUY", 0, 5, "MARKET")

print(limit_order.order_type)
print(market_order.order_type)