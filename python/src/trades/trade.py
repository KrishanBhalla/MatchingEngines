from numpy import datetime64


class Trade():
    """ A concrete class to contain information pertaining to trades.

    Attributes:
    -- time -> the timestamp of the trade
    -- price -> the price of the trade
    -- quantity -> the number of shares traded.
    """

    def __init__(self, datetime: datetime64, price: float, quantity: quantity):

        self.datetime = datetime
        self.price = price
        self.quantity = quantity
