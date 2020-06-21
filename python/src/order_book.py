from python.src.orders import BaseOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderStatus
from python.src.exceptions import InvalidOrderDirectionException
from python.src.trades import Trade
from sortedcontainers import SortedKeyList
from collections import deque
from typing import Optional, List
import numpy as np
import matplotlib.pyplot as plt


class OrderBook:
    """ An order book for a single instrument.

    Attributes:
    --bids -> A PriorityQueue sorted by price to contain all bids.
    --asks -> A PriorityQueue sorted by price to contain all asks.
    --best_bid -> A bid which is first in line to be executed.
    --best_ask -> An ask which is first in line to be executed
    --attempt_match -> A boolean checking whether a match should be attempted.
    --trades -> A record of all completed crossings.
    --complete_orders -> A record of completed orders.
    """

    def __init__(self):
        self.bids = SortedKeyList(key=lambda x: -x.price)
        self.asks = SortedKeyList(key=lambda x: x.price)
        self.best_bid: Optional[BaseOrder] = None
        self.best_ask: Optional[BaseOrder] = None
        self.attempt_match = False
        self.trades: deque = deque()
        self.complete_orders: deque = deque()

    def add_bid(self, order: BaseOrder) -> None:
        """ Adding a bid to the order book

        If there is no best bid, the order must be it,
        else we compare the order with the best bid
        and update, placing the lower bid price into the book.
        We use bisect right to ensure ordering by time when prices match
        """
        best_bid = self.best_bid
        if not best_bid:
            self.best_bid = order
            self.attempt_match = True
        elif order.price <= best_bid.price:
            self.bids.add(order)
        else:
            self.bids.add(best_bid)
            self.best_bid = order
            self.attempt_match = True

    def add_ask(self, order: BaseOrder) -> None:
        """ Adding an ask to the order book

        If there is no best ask, the order must be it,
        else we compare the order with the best ask
        and update, placing the higher ask price into the book.
        """
        best_ask = self.best_ask
        if not best_ask:
            self.best_ask = order
            self.attempt_match = True
        elif order.price >= best_ask.price:
            self.asks.add(order)
        else:
            self.asks.add(best_ask)
            self.best_ask = order
            self.attempt_match = True

    def add_order(self, order: BaseOrder) -> None:
        if order.order_direction == OrderDirection.buy:
            self.add_bid(order)
        elif order.order_direction == OrderDirection.sell:
            self.add_ask(order)
        else:
            raise InvalidOrderDirectionException()

    def match(self) -> None:
        """ Attempt to match orders.

        If possible, match orders and replace the best bid and best ask
        as needed.
        Continue matching until you no longer can.

        If no match occurs, update so that no match is attempted until
        conditions change.
        """
        while self.attempt_match and self.best_bid and self.best_ask:

            self.attempt_match = False
            best_bid = self.best_bid
            best_ask = self.best_ask
            if best_bid.price >= best_ask.price:
                execution_price = (best_bid.price +
                                   best_ask.price) / 2

                matched_quantity = min(best_ask.unfilled_quantity,
                                       best_bid.unfilled_quantity)

                trade = Trade(datetime=np.datetime64("now"),
                              price=execution_price,
                              quantity=matched_quantity)

                best_bid.update_on_trade(trade)
                best_ask.update_on_trade(trade)
                self.trades.append(trade)

                if best_bid.status != OrderStatus.live:
                    self.complete_orders.append(best_bid)
                    if self.bids:
                        self.best_bid = self.bids.pop(0)
                        self.attempt_match = True
                    else:
                        self.best_bid = None

                if best_ask.status != OrderStatus.live:
                    self.complete_orders.append(best_ask)
                    if self.asks:
                        self.best_ask = self.asks.pop(0)
                        self.attempt_match = True
                    else:
                        self.best_ask = None
            else:
                break
        self.attempt_match = False

    def plot_order_book(self) -> None:
        """ Create a line plot showing order book volume and prices"""

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title("Limit Order Book")

        ax.set_xlabel("Price")
        ax.set_ylabel("Quantity")

        if self.best_bid:
            # Cumulative bid volume
            bids = [self.best_bid.quantity] + \
                [bid.quantity for bid in self.bids]
            bids = list(np.cumsum(bids))
            bids.reverse()
            # Bid prices
            bid_prices = [bid.price for bid in self.bids]
            bid_prices.reverse()
            bid_prices += [self.best_bid.price]

        else:
            return None

        if self.best_ask:
            # Cumulative ask volume
            asks = [self.best_ask.quantity]
            asks += [ask.quantity for ask in self.asks]
            asks = list(np.cumsum(asks))
            # Ask prices
            ask_prices = [self.best_ask.price] + \
                [ask.price for ask in self.asks]
        else:
            return None

        # Draw
        ax.step(bid_prices, bids, color='green')
        ax.step(ask_prices, asks, color='red')

        ax.set_xlim([min(bid_prices),
                     max(ask_prices)])
        plt.savefig("images/order_book.png")

    def plot_executions(self) -> None:
        """ Create a line plot showing historic executions """

        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle("Historic Executions")

        ax1.set_xlabel("Time")
        ax1.set_ylabel("Execution Price")

        ax2.set_xlabel("Time")
        ax2.set_ylabel("Executed Quantity")

        # Draw
        times = [t.datetime for t in self.trades]
        ax1.plot(times,
                 [t.price for t in self.trades])

        ax2.plot(times,
                 [t.quantity for t in self.trades])

        ax1.set_xlim([min(times), max(times)])
        ax2.set_xlim([min(times), max(times)])
        plt.savefig("images/executions.png")
