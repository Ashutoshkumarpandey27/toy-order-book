class Order:
    def __init__(self, order_id, side, price, quantity, order_type="LIMIT"):
        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")

        if order_type not in ("LIMIT", "MARKET"):
            raise ValueError("Order type must be LIMIT or MARKET")

        if order_type == "LIMIT" and price <= 0:
            raise ValueError("Limit order price must be positive")

        if order_type == "MARKET" and price < 0:
            raise ValueError("Market order price cannot be negative")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity
        self.order_type = order_type