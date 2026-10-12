from order import Order

try:
    order1 = Order(1, "BUY", 100, 10)
    print("Valid order:", order1.price)

    order2 = Order(2, "SELL", -5, 10)
    print("Invalid order:", order2.price)

except ValueError as e:
    print("Order rejected:", e)

print("Program continues...")