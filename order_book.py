
class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trades = []
        self.last_traded_price = None

    def add_order(self, order):
        # Reject duplicate IDs across active orders
        for existing_order in self.buy_orders + self.sell_orders:
            if existing_order.order_id == order.order_id:
                raise ValueError("Duplicate order ID")

        # Process MARKET orders immediately
        if order.order_type == "MARKET":
            self._process_market_order(order)
            return

        # Add LIMIT orders without automatic matching
        if order.side == "BUY":
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)

    def cancel_order(self, order_id):
        for orders in (self.buy_orders, self.sell_orders):
            for order in orders:
                if order.order_id == order_id:
                    orders.remove(order)
                    print("Order cancelled:", order_id)
                    return

        print("Order not found:", order_id)

    def sort_buy_orders(self):
        # Highest price first; stable sort preserves time priority
        self.buy_orders.sort(
            key=lambda order: order.price,
            reverse=True
        )

    def sort_sell_orders(self):
        # Lowest price first; stable sort preserves time priority
        self.sell_orders.sort(
            key=lambda order: order.price
        )

    def get_best_bid(self):
        if not self.buy_orders:
            return None

        return max(order.price for order in self.buy_orders)

    def get_best_ask(self):
        if not self.sell_orders:
            return None

        return min(order.price for order in self.sell_orders)

    def get_spread(self):
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if best_bid is None or best_ask is None:
            return None

        return best_ask - best_bid

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

    def _execute_trade(self, buy_order, sell_order, price):
        trade_quantity = min(
            buy_order.quantity,
            sell_order.quantity
        )

        trade = {
            "buy_order_id": buy_order.order_id,
            "sell_order_id": sell_order.order_id,
            "price": price,
            "quantity": trade_quantity
        }

        self.trades.append(trade)
        self.last_traded_price = price

        print("Trade executed!")
        print("Trade details:", trade)

        buy_order.quantity -= trade_quantity
        sell_order.quantity -= trade_quantity

        return trade_quantity

    def _process_market_order(self, order):
        # MARKET BUY matches the cheapest SELL orders first.
        # MARKET SELL matches the highest BUY orders first.
        if order.side == "BUY":
            self.sort_sell_orders()
            opposite_orders = self.sell_orders
        else:
            self.sort_buy_orders()
            opposite_orders = self.buy_orders

        while order.quantity > 0 and opposite_orders:
            best_opposite = opposite_orders[0]
            trade_price = best_opposite.price

            if order.side == "BUY":
                self._execute_trade(
                    order,
                    best_opposite,
                    trade_price
                )
            else:
                self._execute_trade(
                    best_opposite,
                    order,
                    trade_price
                )

            if best_opposite.quantity == 0:
                opposite_orders.pop(0)

        # Custom policy: rest any remainder at the last traded price.
        if order.quantity > 0:
            if self.last_traded_price is None:
                print(
                    "Market order could not execute: "
                    "no opposite orders or last traded price available. "
                    "Remaining quantity was not added to the book."
                )
                return

            order.price = self.last_traded_price
            order.order_type = "LIMIT"

            if order.side == "BUY":
                self.buy_orders.append(order)
            else:
                self.sell_orders.append(order)

            print(
                "Unfilled quantity rested as LIMIT order at:",
                order.price,
                "| Remaining quantity:",
                order.quantity
            )

        # Match any crossed resting orders after processing the market order.
        self.match_orders()

    def match_orders(self):
        self.sort_buy_orders()
        self.sort_sell_orders()

        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]

            # Stop when the best prices do not cross.
            if best_buy.price < best_sell.price:
                print("No more matching possible.")
                break

            # Execute at the resting SELL order's price.
            self._execute_trade(
                best_buy,
                best_sell,
                best_sell.price
            )

            if best_buy.quantity == 0:
                self.buy_orders.pop(0)

            if best_sell.quantity == 0:
                self.sell_orders.pop(0)

    def get_total_traded_volume(self):
        return sum(
            trade["quantity"] for trade in self.trades
        )

    def get_vwap(self):
        if not self.trades:
            return None

        total_value = sum(
            trade["price"] * trade["quantity"]
            for trade in self.trades
        )

        total_quantity = self.get_total_traded_volume()

        return total_value / total_quantity

    def get_market_depth(self):
        buy_depth = {}
        sell_depth = {}

        for order in self.buy_orders:
            buy_depth[order.price] = (
                buy_depth.get(order.price, 0)
                + order.quantity
            )

        for order in self.sell_orders:
            sell_depth[order.price] = (
                sell_depth.get(order.price, 0)
                + order.quantity
            )

        return {
            "BUY": dict(sorted(
                buy_depth.items(),
                reverse=True
            )),
            "SELL": dict(sorted(
                sell_depth.items()
            ))
        }

    def get_cumulative_market_depth(self):
        depth = self.get_market_depth()

        cumulative_depth = {
            "BUY": {},
            "SELL": {}
        }

        for side in ("BUY", "SELL"):
            running_quantity = 0

            for price, quantity in depth[side].items():
                running_quantity += quantity
                cumulative_depth[side][price] = running_quantity

        return cumulative_depth

    def get_order_book_stats(self):
        total_buy_quantity = sum(
            order.quantity for order in self.buy_orders
        )

        total_sell_quantity = sum(
            order.quantity for order in self.sell_orders
        )

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
                "Type:", order.order_type,
                "Price:", order.price,
                "Quantity:", order.quantity
            )

        print("SELL ORDERS:")

        for order in self.sell_orders:
            print(
                "ID:", order.order_id,
                "Type:", order.order_type,
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
