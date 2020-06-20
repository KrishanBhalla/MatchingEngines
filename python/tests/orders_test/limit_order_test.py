from python.src.orders import LimitOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderType
from python.src.enums import OrderStatus
from python.src.trades import Trade
from python.src.exceptions import InvalidOrderDirectionException
import numpy as np
import pytest


def test_limit_order_buy():
    instrument_id = "AAPL"
    order_direction = OrderDirection.buy
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)

    assert limit_order.quantity == quantity, "Test failed, incorrect quantity"
    assert limit_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert limit_order.price == price, "Test failed, incorrect price"
    assert limit_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert limit_order.order_type == OrderType.limit, "Test failed, incorrect order type"
    assert limit_order.unfilled_quantity == quantity, "Test failed, incorrect unfilled quantity"
    pass


def test_limit_order_sell():
    instrument_id = "AAPL"
    order_direction = OrderDirection.sell
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)

    assert limit_order.quantity == quantity, "Test failed, incorrect quantity"
    assert limit_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert limit_order.price == price, "Test failed, incorrect price for limit order"
    assert limit_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert limit_order.order_type == OrderType.limit, "Test failed, incorrect order type"
    assert limit_order.unfilled_quantity == quantity, "Test failed, incorrect unfilled quantity"
    pass


def test_limit_order_buy_can_handle_trade():
    instrument_id = "AAPL"
    order_direction = OrderDirection.buy
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=10)
    limit_order.update_on_trade(trade)
    assert limit_order.quantity == quantity, "Test failed, incorrect quantity"
    assert limit_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert limit_order.price == price, "Test failed, incorrect price"
    assert limit_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert limit_order.order_type == OrderType.limit, "Test failed, incorrect order type"
    assert limit_order.fill_info, "Test failed, no fill info"
    assert limit_order.unfilled_quantity == quantity - \
        10, "Test failed, incorrect unfilled quantity"
    pass


def test_limit_order_sell_can_handle_trade():
    instrument_id = "AAPL"
    order_direction = OrderDirection.sell
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=10)
    limit_order.update_on_trade(trade)
    assert limit_order.quantity == quantity, "Test failed, incorrect quantity"
    assert limit_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert limit_order.price == price, "Test failed, incorrect price for limit order"
    assert limit_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert limit_order.order_type == OrderType.limit, "Test failed, incorrect order type"
    assert limit_order.fill_info, "Test failed, no fill info"
    assert limit_order.unfilled_quantity == quantity - \
        10, "Test failed, incorrect unfilled quantity"
    pass


def test_limit_order_sell_can_handle_multiple_trades_to_comletion():
    instrument_id = "AAPL"
    order_direction = OrderDirection.sell
    quantity = 100
    price = 10
    limit_order = LimitOrder(instrument_id=instrument_id,
                             order_direction=order_direction,
                             quantity=quantity,
                             price=price)
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=10)
    limit_order.update_on_trade(trade)
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=90)
    limit_order.update_on_trade(trade)
    assert limit_order.quantity == quantity, "Test failed, incorrect quantity"
    assert limit_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert limit_order.price == price, "Test failed, incorrect price for limit order"
    assert limit_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert limit_order.order_type == OrderType.limit, "Test failed, incorrect order type"
    assert limit_order.fill_info, "Test failed, no fill info"
    assert limit_order.unfilled_quantity == 0, "Test failed, incorrect unfilled quantity"
    assert limit_order.status == OrderStatus.filled, "Test failed, incorrect status"
    pass
