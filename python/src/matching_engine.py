from typing import Dict, Type
from python.src.order_book import OrderBook
from python.src.orders import BaseOrder
from collections import deque
import threading
import logging


class MatchingEngine():
    """ A concrete class to route orders to the relevant book.

    Attributes:
    -- order_books -> A dict of order books, one per instrument
    -- orders -> All orders queued to be processed
    -- processed_orders -> orders that have been processed
    -- live -> a switch to stop processing.
    """

    def __init__(self):

        self.order_books: Dict[str, OrderBook] = {}
        self.orders: deque = deque()
        self.processed_orders: deque = deque()
        self.live: bool = True

    def match(self):

        while self.orders:
            order = self.orders.popleft()
            instrument_id = order.instrument_id

            order_books = self.order_books
            if instrument_id in order_books.keys():
                order_book = order_books[instrument_id]
                order_book.add_order(order)
                order_book.match()
            else:
                order_book = OrderBook()
                order_book.add_order(order)
                order_books[instrument_id] = order_book

            self.processed_orders.append(order)

    def add_order(self, order: BaseOrder):
        self.orders.append(order)

    def process(self):
        logging.info("Process: Thread starting")
        while self.live:
            if self.orders:
                self.match()

        logging.info("Process: Thread finishing")

    def run(self):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        thread = threading.Thread(target=self.process)
        thread.start()
        logging.info("Run : wait for the thread to finish")
        logging.info("Run : all done")
