from .base_order import BaseOrder
from enums import OrderDirection
from enums import OrderType


class MarketOrder(BaseOrder):
    """ A market order tries to execute at a any price.

    We implement it separately to limit orders, though it will
    fulfill a similar function.
    """

    def __init__(self,
                 instrument_id: str,
                 order_direction: OrderDirection,
                 quantity: int
                 ):

        super().__init__(instrument_id=instrument_id,
                         order_direction=order_direction,
                         order_type=OrderType.market,
                         quantity=quantity)
