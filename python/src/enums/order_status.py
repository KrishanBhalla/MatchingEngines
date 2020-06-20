from enum import Enum, auto

class OrderStatus(Enum):
    """ Implements order statuses

    -- live - an order presently in the book
    -- filled - an order that has completed filling.
    -- canceled - an order that was cancelled before complete fill.
    """
    live = auto()
    filled = auto()
    canceled = auto()