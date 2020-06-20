from enum import Enum, auto

class OrderType(Enum):
    """ Implements order types

    -- limit - an order in the book to trade a security at at worst the limit price set
    -- market - an order in the book to trade the security at the realised market price.
    -- cancel - an order to the engine to cancel a previous order if possible.
    -- amend - an order that can update an existing order.
    """
    limit = auto()
    market = auto()
    cancel = auto()
    amend = auto()