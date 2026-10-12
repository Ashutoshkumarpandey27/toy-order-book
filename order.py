class Order:
    def __init__(self, order_id, side, price, quantity):
        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity