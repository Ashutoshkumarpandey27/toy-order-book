
class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trades = []

    def add_order(self, order):
        # Reject duplicate IDs across active BUY and SELL orders
        for existing_order in self.buy_orders + self.sell_orders:
            if existing_order.order_id == order.order_id:
                raise ValueError("Duplicate order ID")

        # Add order to the appropriate side
        if order.side == "BUY":
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)

    def cancel_order(self, order_id):
        # Search and cancel BUY order
        for order in self.buy_orders:
            if order.order_id == order_id:
                self.buy_orders.remove(order)
                print("Order cancelled:", order_id)
                return

        # Search and cancel SELL order
        for order in self.sell_orders:
            if order.order_id == order_id:
                self.sell_orders.remove(order)
                print("Order cancelled:", order_id)
                return

        print("Order not found:", order_id)

    def sort_buy_orders(self):
        # Highest BUY price first; stable sort preserves time priority
        self.buy_orders.sort(
            key=lambda order: order.price,
            reverse=True
        )

    def get_best_bid(self):
        # Return the highest BUY price
        if not self.buy_orders:
            return None

        return max(order.price for order in self.buy_orders)

    def get_best_ask(self):
        # Return the lowest SELL price
        if not self.sell_orders:
            return None

        return min(order.price for order in self.sell_orders)

    def get_spread(self):
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        # Spread cannot be calculated if either side is empty
        if best_bid is None or best_ask is None:
            return None

        return best_ask - best_bid

    def sort_sell_orders(self):
        # Lowest SELL price first; stable sort preserves time priority
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

        # Match while compatible orders exist
        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]

            # Stop if prices do not cross
            if best_buy.price < best_sell.price:
                print("No more matching possible.")
                break

            # Determine traded quantity
            trade_quantity = min(
                best_buy.quantity,
                best_sell.quantity
            )

            # Record the executed trade
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

    def get_total_traded_volume(self):
        # Sum the quantities of all executed trades
        total_volume = 0

        for trade in self.trades:
            total_volume += trade["quantity"]

        return total_volume

    def get_market_depth(self):
        buy_depth = {}
        sell_depth = {}

        # Group BUY orders by price
        for order in self.buy_orders:
            if order.price not in buy_depth:
                buy_depth[order.price] = 0

            buy_depth[order.price] += order.quantity

        # Group SELL orders by price
        for order in self.sell_orders:
            if order.price not in sell_depth:
                sell_depth[order.price] = 0

            sell_depth[order.price] += order.quantity

        # Sort BUY prices from highest to lowest
        buy_depth = dict(
            sorted(buy_depth.items(), reverse=True)
        )

        # Sort SELL prices from lowest to highest
        sell_depth = dict(
            sorted(sell_depth.items())
        )

        return {
            "BUY": buy_depth,
            "SELL": sell_depth
        }

    def get_cumulative_market_depth(self):
        # Get the regular market depth
        depth = self.get_market_depth()

        cumulative_depth = {
            "BUY": {},
            "SELL": {}
        }

        # Calculate cumulative BUY quantities
        running_quantity = 0

        for price, quantity in depth["BUY"].items():
            running_quantity += quantity
            cumulative_depth["BUY"][price] = running_quantity

        # Calculate cumulative SELL quantities
        running_quantity = 0

        for price, quantity in depth["SELL"].items():
            running_quantity += quantity
            cumulative_depth["SELL"][price] = running_quantity

        return cumulative_depth

    def get_order_book_stats(self):
        # Calculate total BUY and SELL quantities
        total_buy_quantity = 0
        total_sell_quantity = 0

        for order in self.buy_orders:
            total_buy_quantity += order.quantity

        for order in self.sell_orders:
            total_sell_quantity += order.quantity

        # Return order book statistics
        return {
            "active_buy_orders": len(self.buy_orders),
            "active_sell_orders": len(self.sell_orders),
            "total_buy_quantity": total_buy_quantity,
            "total_sell_quantity": total_sell_quantity,
            "total_active_orders": (
                len(self.buy_orders) + len(self.sell_orders)
            )
        }

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
