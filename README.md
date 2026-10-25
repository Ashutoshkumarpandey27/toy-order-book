# Toy Order Book — Python Matching Engine

A Python-based educational order book that simulates how buy and sell orders are stored, prioritized, and matched in a financial market.

This project was built to explore order matching, market microstructure fundamentals, data structures, automated testing, and performance measurement.

**Note:** This is a simulation. It does not connect to a live stock exchange or execute real trades.

## Features

- Limit and market order handling
- Price-time priority
- Partial order execution
- Order cancellation
- Input validation and duplicate active order ID protection
- Trade history
- Best bid, best ask, and bid-ask spread
- Market depth and cumulative market depth
- Total traded volume and volume-weighted average price (VWAP)
- Automated tests using pytest
- Order insertion benchmark

## Tech Stack

- Python
- pytest
- Git and GitHub

## Project Structure

```text
toy-order-book/
├── order.py
├── order_book.py
├── main.py
├── benchmark.py
├── tests/
│   ├── test_order.py
│   └── test_order_book.py
├── test_order_types.py
├── README.md
└── .gitignore
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AshutoshkumarPandey27/toy-order-book.git
cd toy-order-book
```

### 2. Create and activate a virtual environment

Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install pytest

```bash
python -m pip install pytest
```

## Run the Project

Run the demonstration:

```bash
python main.py
```

Run the automated tests:

```bash
python -m pytest -v
```

Run the insertion benchmark:

```bash
python benchmark.py
```

## Matching Logic

The matching engine follows these basic rules:

1. Buy orders are prioritized by highest price.
2. Sell orders are prioritized by lowest price.
3. Orders at the same price follow arrival order.
4. Crossing orders can execute partially or completely.
5. Market orders consume available opposite-side liquidity immediately; any unfilled remainder is cancelled.
6. The simulator records completed trades and provides basic market analytics.

## Testing

The current test suite has **71 passing tests**, based on the latest local test run.

Run the tests again in your environment to verify the current version:

```bash
python -m pytest -v
```

## Benchmark

In one local benchmark run, the project inserted 10,000 orders in approximately **0.020 seconds**, with a reported throughput of around **499,136 orders per second**.

Benchmark results vary with hardware, Python version, system load, and implementation changes. This benchmark measures the insertion workload, not production exchange performance or full matching throughput.

## Limitations

- Educational simulation only; no live exchange or broker integration.
- No live market data feed or real-money trading.
- Uses simplified in-memory order-book data structures.
- Does not implement production exchange networking, persistence, risk controls, or concurrency guarantees.

## Learning Outcomes

This project provided practical experience with object-oriented Python, order validation, matching algorithms, data structures, unit testing, benchmarking, and version control.

## Author

**Ashutosh Kumar Pandey**

GitHub: https://github.com/AshutoshkumarPandey27/toy-order-book
