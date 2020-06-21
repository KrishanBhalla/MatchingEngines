from typing import Dict, List
from python.src.order_book import OrderBook
from python.src.orders import BaseOrder
import threading
import logging


class MatchingEngine():

    def __init__(self):

        self.order_books: Dict[str, OrderBook] = {}
        self.orders: List[BaseOrder] = []
        self.processed_orders: List[BaseOrder] = []

    def match(self):

        while self.orders:
            order = self.orders.pop(0)
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
        while True:
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
