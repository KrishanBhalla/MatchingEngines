from .base_order import BaseOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderType
from python.src.exceptions import InvalidOrderDirectionException


class MarketOrder(BaseOrder):
    """ A market order tries to execute immediately any price.
    """

    def __init__(self,
                 instrument_id: str,
                 order_direction: OrderDirection,
                 quantity: int
                 ):

        if order_direction == OrderDirection.buy:
            price = float("inf")
        elif order_direction == OrderDirection.sell:
            price = 0
        else:
            raise InvalidOrderDirectionException()

        super().__init__(instrument_id=instrument_id,
                         order_direction=order_direction,
                         order_type=OrderType.market,
                         quantity=quantity,
                         price=price)
