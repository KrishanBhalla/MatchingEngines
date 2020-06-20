from enums import OrderDirection
from enums import OrderType
from enums import OrderStatus
from abc import ABC
from trades import Trade
from typing import List


class BaseOrder(ABC):
    """ An abstract class define regular orders.

    Class Attributes:
    -- a counter for the total number of orders recieved. This acts as an order_id in cases
    when an order_id is not provided (all but cancels).

    Instance Attributes
    -- instrument_id -> A unique identifier for the instrument
    -- order_id -> A unique id defining the order. On cancels this will be referenced.
    -- order_direction -> whether the order is a Buy, Sell, or Cancel
    -- order_type -> denoting how the order is implemented - limit order, market order etc.
    -- price -> the limit price of the orders. For market orders these may be infinite
    -- quantity -> How many shares to execute.
    -- unfilled_quantity -> How many shares have been yet to be executed.
    -- fill_info -> A dict mapping execution times to Price * Quantity.
        This will be updated over time.
    -- status -> an OrderStatus value to reference whether an order is still live (in the market)
    """

    counter: int = 1

    def __init__(self,
                 instrument_id: str,
                 order_direction: OrderDirection,
                 quantity: int,
                 order_type: OrderType,
                 price: float
                 ):

        self.instrument_id = instrument_id
        self.order_direction = order_direction
        self.order_type = order_type
        self.quantity = quantity
        self.unfilled_quantity = quantity
        self.price = price

        self.counter += 1
        self.order_id: int = self.counter
        self.fill_info: List[Trade] = []
        self.status: bool = OrderStatus.live

    def update_on_trade(self, trade: Trade) -> None:
        """ On a trade occuring, update the order."""

        self.fill_info.append(trade)
        self.unfilled_quantity -= trade.quantity

        if self.unfilled_quantity != 0:
            self.status = OrderStatus.filled
