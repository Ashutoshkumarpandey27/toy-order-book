
class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trades = []

    def add_order(self, order):
        # Reject duplicate IDs across BUY and SELL orders
        for existing_order in self.buy_orders + self.sell_orders:
            if existing_order.order_id == order.order_id:
                raise ValueError("Duplicate order ID")

        # Add order to the appropriate side
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
        # Highest BUY price first; stable sorting preserves arrival order
        self.buy_orders.sort(
            key=lambda order: order.price,
            reverse=True
        )

    def sort_sell_orders(self):
        # Lowest SELL price first; stable sorting preserves arrival order
        self.sell_orders.sort(
            key=lambda order: order.price
        )

    def check_matching(self):
        if not self.buy_orders or not self.sell_orders:
            print("Not enough orders to match.")
            return

        self.sort_buy_orders()
        self.sort_sell_orders()

        best_buy = self.buy_orders[0]
        best_sell = self.sell_orders[0]

        if best_buy.price >= best_sell.price:
            print("Orders can match!")
        else:
            print("No match available.")

    def match_orders(self):
        # Sort orders before matching
        self.sort_buy_orders()
        self.sort_sell_orders()

        # Match as long as compatible orders exist
        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]

            # Stop if prices do not cross
            if best_buy.price < best_sell.price:
                print("No more matching possible.")
                break

            # Determine the quantity traded
            trade_quantity = min(
                best_buy.quantity,
                best_sell.quantity
            )

            # Record the trade
            trade = {
                "buy_order_id": best_buy.order_id,
                "sell_order_id": best_sell.order_id,
                "price": best_sell.price,
                "quantity": trade_quantity
            }

            self.trades.append(trade)

            print("Trade executed!")
            print("Trade details:", trade)

            # Update remaining quantities
            best_buy.quantity -= trade_quantity
            best_sell.quantity -= trade_quantity

            # Remove fully filled orders
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

    def display_trades(self):
        print("TRADE HISTORY:")

        if not self.trades:
            print("No trades executed yet.")
            return

        for trade in self.trades:
            print(
                "BUY ID:", trade["buy_order_id"],
                "| SELL ID:", trade["sell_order_id"],
                "| Price:", trade["price"],
                "| Quantity:", trade["quantity"]
            )
