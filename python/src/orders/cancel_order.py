from python.src.enums import OrderType
from python.src.enums import OrderStatus
from python.src.enums import OrderDirection
from python.src.exceptions import InvalidOrderDirectionException
from python.src.orders import BaseOrder
from typing import Type


class CancelOrder():
    """ An concrete class implementing cancel functionality.

        Instance Attributes
        -- instrument_id -> A unique identifier for the instrument
        -- order_id -> A unique id defining the order.
        -- order_type -> denoting how the order is implemented - limit order, market order etc.
        -- cancel_success -> a boolean checking whether the relevant order was cancelled
        -- order_direction -> whether the order is a Buy or Sell

    """

    def __init__(self,
                 instrument_id: str,
                 order_id: int,
                 order_direction: OrderDirection
                 ):

        self.instrument_id = instrument_id
        self.order_id = order_id
        self.order_type: OrderType = OrderType.cancel
        self.order_direction = order_direction
        self.cancel_success: bool = False

    def cancel_order(self, order: Type[BaseOrder]) -> None:
        """ Modify in place the Order to be cancelled """

        if order.status == OrderStatus.live:
            order.status = OrderStatus.cancelled
            self.cancel_success = True
