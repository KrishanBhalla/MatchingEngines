
class InvalidOrderDirectionException(Exception):
    """Raised when the order direction is not Buy or Sell"""

    def __init__(self):
        message = "Direction should be from the OrderDirectionEnum, and be Buy Or Sell only"
        super().__init__(message)
