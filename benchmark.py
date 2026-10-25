
import time
from order import Order
from order_book import OrderBook


def benchmark_order_insertion(number_of_orders):
    book = OrderBook()

    start_time = time.perf_counter()

    for i in range(number_of_orders):
        # Non-crossing BUY orders avoid trade execution.
        order = Order(
            order_id=i,
            side="BUY",
            price=100 - (i % 50),
            quantity=10
        )
        book.add_order(order)

    elapsed_time = time.perf_counter() - start_time

    print(f"Orders added: {number_of_orders}")
    print(f"Time taken: {elapsed_time:.6f} seconds")
    print(f"Orders per second: {number_of_orders / elapsed_time:.0f}")


if __name__ == "__main__":
    for count in (1_000, 5_000, 10_000):
        print(f"\n--- Benchmark: {count} orders ---")
        benchmark_order_insertion(count)
