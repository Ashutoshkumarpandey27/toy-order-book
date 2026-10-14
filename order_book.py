
class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == "BUY":
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)


    
    def cancel_order(self, order_id):
        for order in self.buy_orders:
            if order.order_id == order_id:
                self.buy_orders.remove(order)
                print("Order cancelled:", order_id)
                return

        for order in self.sell_orders:
            if order.order_id == order_id:
                self.sell_orders.remove(order)
                print("Order cancelled:", order_id)
                return

        print("Order not found:", order_id)


    def sort_buy_orders(self):
        # Highest BUY price gets priority
        self.buy_orders.sort(
            key=lambda order: order.price,
            reverse=True
        )

    def sort_sell_orders(self):
        # Lowest SELL price gets priority
        self.sell_orders.sort(
            key=lambda order: order.price
        )

    def check_matching(self):
        # Check whether both sides have orders
        if not self.buy_orders or not self.sell_orders:
            print("Not enough orders to match.")
            return

        # Get the highest BUY and lowest SELL
        best_buy = self.buy_orders[0]
        best_sell = self.sell_orders[0]

        # Check price compatibility
        if best_buy.price >= best_sell.price:
            print("Orders can match!")
        else:
            print("No match available.")
    
    def match_orders(self):
        # Sort both sides before matching
        self.sort_buy_orders()
        self.sort_sell_orders()

        # Keep matching while both sides have orders
        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]

            # Stop if prices are not compatible
            if best_buy.price < best_sell.price:
                print("No more matching possible.")
                break

            # Execute the smaller quantity
            trade_quantity = min(
                best_buy.quantity,
                best_sell.quantity
            )

            print("Trade executed!")
            print("Trade quantity:", trade_quantity)

            # Reduce remaining quantities
            best_buy.quantity -= trade_quantity
            best_sell.quantity -= trade_quantity

            # Remove completely filled orders
            if best_buy.quantity == 0:
                self.buy_orders.pop(0)

            if best_sell.quantity == 0:
                self.sell_orders.pop(0)


    def display_orders(self):
        print("BUY ORDERS:")

        for order in self.buy_orders:
            print(
                "ID:", order.order_id,
                "Price:", order.price,
                "Quantity:", order.quantity
            )

        print("SELL ORDERS:")

        for order in self.sell_orders:
            print(
                "ID:", order.order_id,
                "Price:", order.price,
                "Quantity:", order.quantity
            )

