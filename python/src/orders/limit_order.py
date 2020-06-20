from enums import OrderDirection
from enums import OrderType
from .base_order import BaseOrder


class LimitOrder(BaseOrder):
    """ A limit order tries to execute at a certain price or better.

    """

    def __init__(self,
                 instrument_id: str,
                 order_direction: OrderDirection,
                 quantity: int,
                 price: float
                 ):

        super().__init__(instrument_id=instrument_id,
                         order_direction=order_direction,
                         order_type=OrderType.limit,
                         quantity=quantity,
                         price=price)
