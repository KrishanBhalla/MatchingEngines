from python.src.orders import MarketOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderType
from python.src.trades import Trade
from python.src.exceptions import InvalidOrderDirectionException
import numpy as np
import pytest


def test_market_order_buy():
    instrument_id = "AAPL"
    order_direction = OrderDirection.buy
    quantity = 100
    market_order = MarketOrder(instrument_id=instrument_id,
                               order_direction=order_direction,
                               quantity=quantity)

    assert market_order.quantity == quantity, "Test failed, incorrect quantity"
    assert market_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert market_order.price == float("inf"), "Test failed, incorrect price"
    assert market_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert market_order.order_type == OrderType.market, "Test failed, incorrect order type"
    assert market_order.unfilled_quantity == quantity, "Test failed, incorrect unfilled quantity"
    pass


def test_market_order_sell():
    instrument_id = "AAPL"
    order_direction = OrderDirection.sell
    quantity = 100
    market_order = MarketOrder(instrument_id=instrument_id,
                               order_direction=order_direction,
                               quantity=quantity)

    assert market_order.quantity == quantity, "Test failed, incorrect quantity"
    assert market_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert market_order.price == 0, "Test failed, incorrect price for market order"
    assert market_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert market_order.order_type == OrderType.market, "Test failed, incorrect order type"
    assert market_order.unfilled_quantity == quantity, "Test failed, incorrect unfilled quantity"
    pass


def test_market_order_incorrect_order_direction():
    with pytest.raises(InvalidOrderDirectionException):
        instrument_id = "AAPL"
        order_direction = OrderDirection.test
        quantity = 100
        MarketOrder(instrument_id=instrument_id,
                    order_direction=order_direction,
                    quantity=quantity)
    pass


def test_market_order_buy_can_handle_trade():
    instrument_id = "AAPL"
    order_direction = OrderDirection.buy
    quantity = 100
    market_order = MarketOrder(instrument_id=instrument_id,
                               order_direction=order_direction,
                               quantity=quantity)
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=10)
    market_order.update_on_trade(trade)
    assert market_order.quantity == quantity, "Test failed, incorrect quantity"
    assert market_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert market_order.price == float('inf'), "Test failed, incorrect price"
    assert market_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert market_order.order_type == OrderType.market, "Test failed, incorrect order type"
    assert market_order.fill_info, "Test failed, no fill info"
    assert market_order.unfilled_quantity == quantity - \
        10, "Test failed, incorrect unfilled quantity"


def test_market_order_sell_can_handle_trade():
    instrument_id = "AAPL"
    order_direction = OrderDirection.sell
    quantity = 100
    market_order = MarketOrder(instrument_id=instrument_id,
                               order_direction=order_direction,
                               quantity=quantity)
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=10)
    market_order.update_on_trade(trade)
    assert market_order.quantity == quantity, "Test failed, incorrect quantity"
    assert market_order.order_direction == order_direction, "Test failed, incorrect quantity"
    assert market_order.price == 0, "Test failed, incorrect price for market order"
    assert market_order.instrument_id == instrument_id, "Test failed, incorrect instrument_id"
    assert market_order.order_type == OrderType.market, "Test failed, incorrect order type"
    assert market_order.fill_info, "Test failed, no fill info"
    assert market_order.unfilled_quantity == quantity - \
        10, "Test failed, incorrect unfilled quantity"
