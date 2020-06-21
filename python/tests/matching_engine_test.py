from python.src.matching_engine import MatchingEngine
from python.src.order_book import OrderBook
from python.src.orders import LimitOrder
from python.src.orders import MarketOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderDirection
from python.src.enums import OrderStatus
from python.src.exceptions import InvalidOrderDirectionException
import pytest


def test_matching_engine_init():
    matching_engine = MatchingEngine()

    assert not matching_engine.order_books, "Test Failed: order_books should be empty"
    assert not matching_engine.orders, "Test Failed: orders should be empty"
    assert not matching_engine.processed_orders, "Test Failed: processed_orders should be empty"
    pass


def test_matching_engine_can_match():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (i if i % 2 else -i)) for i in range(10)]

    matching_engine = MatchingEngine()

    for order in limit_orders:
        matching_engine.add_order(order)
    matching_engine.match()
    order_book = matching_engine.order_books[instrument_id]

    assert len(
        matching_engine.order_books) == 1, "Test Failed: There should be 1 order book"
    assert not matching_engine.orders, "Test Failed: There should be no orders"
    assert len(
        matching_engine.processed_orders) == 10, "Test Failed: There should be 10 processed_orders"
    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_matching_engine_can_add_orders():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (i if i % 2 else -i)) for i in range(10)]

    matching_engine = MatchingEngine()

    for order in limit_orders:
        matching_engine.add_order(order)

    assert not matching_engine.order_books, "Test Failed: There should beno order books"
    assert matching_engine.orders, "Test Failed: There should be orders"
    assert len(
        matching_engine.orders) == 10, "Test Failed: There should be 10 orders"
    assert not matching_engine.processed_orders, "Test Failed: There should be no processed_orders"
    pass


def test_matching_engine_can_add_and_process():
    instrument_id = "AAPL"
    quantity = 100
    price = 10
    limit_orders = [LimitOrder(instrument_id=instrument_id,
                               order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                               quantity=quantity,
                               price=price + (i if i % 2 else -i)) for i in range(10)]

    matching_engine = MatchingEngine()

    for order in limit_orders:
        matching_engine.add_order(order)
    matching_engine.match()
    order_book = matching_engine.order_books[instrument_id]

    assert len(
        matching_engine.order_books) == 1, "Test Failed: There should be 1 order book"
    assert not matching_engine.orders, "Test Failed: There should be no orders"
    assert len(
        matching_engine.processed_orders) == 10, "Test Failed: There should be 10 processed_orders"
    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_matching_engine_can_add_and_match_multiple_instruments():
    instrument_id_1 = "AAPL"
    instrument_id_2 = "MSFT"
    quantity = 100
    price = 10
    limit_orders_1 = [LimitOrder(instrument_id=instrument_id_1,
                                 order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                                 quantity=quantity,
                                 price=price + (i if i % 2 else -i)) for i in range(10)]
    limit_orders_2 = [LimitOrder(instrument_id=instrument_id_2,
                                 order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                                 quantity=quantity,
                                 price=price + (i if i % 2 else -i)) for i in range(10)]

    matching_engine = MatchingEngine()

    for order in limit_orders_1 + limit_orders_2:
        matching_engine.add_order(order)

    matching_engine.match()
    order_book = matching_engine.order_books[instrument_id_1]

    assert len(
        matching_engine.order_books) == 2, "Test Failed: There should be 2 order books"
    assert not matching_engine.orders, "Test Failed: There should be no orders"
    assert len(
        matching_engine.processed_orders) == 20, "Test Failed: There should be 20 processed_orders"

    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"

    order_book = matching_engine.order_books[instrument_id_2]

    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass


def test_matching_engine_can_add_and_run_multiple_instruments():
    instrument_id_1 = "AAPL"
    instrument_id_2 = "MSFT"
    quantity = 100
    price = 10
    limit_orders_1 = [LimitOrder(instrument_id=instrument_id_1,
                                 order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                                 quantity=quantity,
                                 price=price + (i if i % 2 else -i)) for i in range(10)]
    limit_orders_2 = [LimitOrder(instrument_id=instrument_id_2,
                                 order_direction=OrderDirection.buy if i % 2 else OrderDirection.sell,
                                 quantity=quantity,
                                 price=price + (i if i % 2 else -i)) for i in range(10)]

    matching_engine = MatchingEngine()

    for order in limit_orders_1 + limit_orders_2:
        matching_engine.add_order(order)

    matching_engine.run()
    matching_engine.live = False
    order_book = matching_engine.order_books[instrument_id_1]

    assert len(
        matching_engine.order_books) == 2, "Test Failed: There should be 2 order books"
    assert not matching_engine.orders, "Test Failed: There should be no orders"
    assert len(
        matching_engine.processed_orders) == 20, "Test Failed: There should be 20 processed_orders"

    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"

    order_book = matching_engine.order_books[instrument_id_2]

    assert not order_book.bids, "Test Failed: There should be no bids after complete matching"
    assert not order_book.asks, "Test Failed: There should be no asks after complete matching"
    assert order_book.best_bid is None, "Test Failed: best_bid should be empty"
    assert order_book.best_ask is None, "Test Failed: best_ask should be empty"
    assert len(
        order_book.trades) == 5, "Test Failed: trades should have 5 orders"
    assert len(
        order_book.complete_orders) == 10, "Test Failed: complete_orders should have all orders"
    assert not order_book.attempt_match, "Test Failed: attempt_match should be False"
    pass
