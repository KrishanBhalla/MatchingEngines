from python.src.order_book import OrderBook
from python.src.orders import LimitOrder
from python.src.orders import MarketOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderDirection
from python.src.enums import OrderStatus
from python.src.exceptions import InvalidOrderDirectionException
import pytest


def test_order_book_init():
    order_book = OrderBook()

    assert not order_book.bids, "Test Failed: bids should be empty"
    assert not order_book.asks, "Test Failed: asks should be empty"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert not order_book.trades, "Test Failed: trades should be empty"
    assert not order_book.complete_orders, "Test Failed: complete_orders should be empty"
    assert not order_book.attempt_match, "Test Failed: attempt_match should default to False"
    pass


def test_order_book_can_add_orders():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (i if i % 2 else -i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    assert len(order_book.bids) == 4, "Test Failed: There should be 5 bids"
    assert len(order_book.asks) == 4, "Test Failed: There should be 5 asks"
    assert order_book.best_bid is not None, "Test Failed: best_bid should not be empty"
    assert order_book.best_ask is not None, "Test Failed: best_ask should not be empty"
    assert order_book.best_bid.price > order_book.best_ask.price, "Test Failed: best prices are not aligned"
    assert all(order_book.bids[i].price > order_book.asks[i].price for i in range(4)), \
        "Test Failed: prices are not aligned"
    assert not order_book.trades, "Test Failed: trades should be empty"
    assert not order_book.complete_orders, "Test Failed: complete_orders should be empty"
    assert order_book.attempt_match, "Test Failed: attempt_match should be True"
    pass


def test_order_book_raise_exception_on_invalid_order():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=OrderDirection.test,
                             quantity=quantity,
                             price=price)
    order_book = OrderBook()

    with pytest.raises(InvalidOrderDirectionException) as exn:
        order_book.add_order(limit_order)
    pass


def test_order_book_can_match_orders():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (i if i % 2 else -i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.match()
    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_order_book_cannot_match_non_crossing_orders():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (-i if i % 2 else i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.match()
    assert len(order_book.bids) == 4, "Test Failed: There should be 5 bids"
    assert len(order_book.asks) == 4, "Test Failed: There should be 5 asks"
    assert order_book.best_bid is not None, "Test Failed: best_bid should not be empty"
    assert order_book.best_ask is not None, "Test Failed: best_ask should not be empty"
    assert order_book.best_bid.price <= order_book.best_ask.price, "Test Failed: best prices are not aligned"
    assert all(order_book.bids[i].price <= order_book.asks[i].price for i in range(4)), \
        "Test Failed: prices are not aligned"
    assert not order_book.trades, "Test Failed: trades should be empty"
    assert not order_book.complete_orders, "Test Failed: complete_orders should be empty"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_order_book_can_match_incomplete_more_asks():
    """ Here there are more asks than bids, so the bids will fill"""
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity - 10 * i,
                               price=price + (i if i % 2 else -i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.match()

    assert not order_book.bids, "Test Failed: There should be no bids after this matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should not be empty"
    assert not order_book.asks, "Test Failed: There should no asks after this matching"
    assert order_book.best_ask is not None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) > 5, "Test Failed: trades should more than 5 trades"
    assert len(
        order_book.complete_orders) < 10, "Test Failed: complete_orders should have fewer than 10 orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_order_book_can_match_incomplete_more_bids():
    """ Here there are more asks than bids, so the bids will fill"""
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if not i % 2 else OrderDirection.sell,
                               quantity=quantity - 10 * i,
                               price=price + (i if not i % 2 else -i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.match()
    assert not order_book.asks, "Test Failed: There should be no asks after this matching"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert not order_book.bids, "Test Failed: There should be  no bids after this matching"
    assert order_book.best_bid is not None, "Test Failed: best_bid should not be empty"
    assert len(
        order_book.trades) > 5, "Test Failed: trades should more than 5 trades"
    assert len(
        order_book.complete_orders) < 10, "Test Failed: complete_orders should have fewer than 10 orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_order_book_can_handle_limit_and_market_orders_together():
    """ Here there are more asks than bids, so the bids will fill"""
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy,
                               quantity=quantity - 10 * i,
                               price=price + i) for i in range(5)]

    market_order = MarketOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.sell,
                               quantity=400)

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.add_order(market_order)
    order_book.match()

    assert not order_book.asks, "Test Failed: There should be no asks after this matching"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert not order_book.bids, "Test Failed: There should be  no bids after this matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: there should be 5 trades"
    assert len(
        order_book.complete_orders) == 6, "Test Failed: complete_orders should have 6 orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_order_book_can_generate_order_book_plot():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (-i if i % 2 else i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.plot_order_book()
    pass


def test_order_book_can_generate_execution_plot():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if not i % 2 else OrderDirection.sell,
                               quantity=quantity - 10 * i,
                               price=price + (i if not i % 2 else -2*i)) for i in range(10)]

    order_book = OrderBook()

    for order in limit_orders:
        order_book.add_order(order)
    order_book.match()
    order_book.plot_executions()
    pass
