from enums import OrderDirection
from enums import OrderType
from .base_order import BaseOrder

class LimitOrder(BaseOrder):
    """ A limit order tries to execute at a certain price or better.

    Attributes
    -- limit_price -> the worst (Highest for Buys, lowest for Sells) price 
    the order can execute at.
    """

    def __init__(self,
                 instrument_id: str,
                 order_direction: OrderDirection,
                 quantity: int,
                 limit_price: float
                 ):
        
        super().__init__(instrument_id=instrument_id,
        order_direction=order_direction,
        order_type = OrderType.limit,
        quantity=quantity)
        self.limit_price = limit_price
