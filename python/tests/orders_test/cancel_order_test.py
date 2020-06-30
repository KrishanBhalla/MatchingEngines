from python.src.orders import CancelOrder
from python.src.orders import LimitOrder
from python.src.enums import OrderType
from python.src.enums import OrderStatus
from python.src.enums import OrderDirection
import numpy as np
import pytest


def test_cancel_order_init_():
    instrument_id = "AAPL"
    order_id = 1
    cancel_order = CancelOrder(instrument_id=instrument_id,
                               order_id=order_id,
                               order_direction=OrderDirection.buy)

    assert not cancel_order.cancel_success, "Test Failed: cancel_success should be false unless an order can be cancelled"
    pass


def test_can_cancel_limit_order():
    instrument_id = "AAPL"
    order_direction = OrderDirection.buy
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)
    limit_order.order_id = 1

    assert limit_order.status == OrderStatus.live, "Test failed: order not live"

    instrument_id = "AAPL"
    order_id = 1
    cancel_order = CancelOrder(instrument_id=instrument_id,
                               order_id=order_id,
                               order_direction=order_direction)

    cancel_order.cancel_order(order=limit_order)

    assert limit_order.status == OrderStatus.cancelled, "Test failed: order not cancelled"
    assert cancel_order.cancel_success, "Test Failed: order not cancelled"
    pass


def test_cannot_cancel_filled_order():
    instrument_id = "AAPL"
    order_direction = OrderDirection.buy
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)
    limit_order.order_id = 1
    limit_order.status = OrderStatus.filled

    instrument_id = "AAPL"
    order_id = 1
    cancel_order = CancelOrder(instrument_id=instrument_id,
                               order_id=order_id,
                               order_direction=order_direction)

    cancel_order.cancel_order(order=limit_order)

    assert limit_order.status == OrderStatus.filled, "Test failed: order cancelled"
    assert not cancel_order.cancel_success, "Test Failed: order cancelled"
    pass
