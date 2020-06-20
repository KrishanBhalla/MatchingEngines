from enum import Enum, auto


class OrderDirection(Enum):
    """ Implements order directions
    -- buy - an order in the market to purchase the security
    -- sell - an order in the market to sell the security
    -- test - an value used exclusively for error checking.
    """
    buy = auto()
    sell = auto()
    test = auto()
