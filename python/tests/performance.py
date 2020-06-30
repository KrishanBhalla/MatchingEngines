from python.src.orders import LimitOrder
from python.src.orders import MarketOrder
from python.src.orders import CancelOrder
from python.src.enums import OrderDirection
from python.src.enums import OrderStatus
from python.src.matching_engine import MatchingEngine
import random
import cProfile
import pstats

num_orders = 10_000


def get_data(n):
    instrument_ids = ["AAPL", "MSFT", "TSLA", "FB", "NFLX"]
    quantity = 100
    price = 40
    m = n // len(instrument_ids)
    output = []
    for instr in instrument_ids:
        buy_limits = [LimitOrder(instrument_id=instr,
                                 order_direction=OrderDirection.buy,
                                 quantity=quantity + random.uniform(-50, 50),
                                 price=price + random.uniform(-2.5, 2.5))
                      for i in range(m//4)]
        sell_limits = [LimitOrder(instrument_id=instr,
                                  order_direction=OrderDirection.sell,
                                  quantity=quantity + random.uniform(-50, 50),
                                  price=price + random.uniform(-2.5, 2.5))
                       for i in range(m//4)]

        buy_markets = [MarketOrder(instrument_id=instr,
                                   order_direction=OrderDirection.buy,
                                   quantity=quantity + random.uniform(-50, 50))
                       for i in range(m//4)]

        sell_markets = [MarketOrder(instrument_id=instr,
                                    order_direction=OrderDirection.sell,
                                    quantity=quantity +
                                    random.uniform(-50, 50))
                        for i in range(m//4)]
        output += buy_limits + sell_limits + buy_markets + sell_markets
        random.shuffle(output)
    return output


orders = get_data(num_orders)
matching_engine = MatchingEngine()
for order in orders:
    matching_engine.add_order(order)
# matching_engine.match()
#  profile
cProfile.run("matching_engine.match()", "prof_file")
p = pstats.Stats("prof_file")
p.strip_dirs().sort_stats(-1).print_stats(10)

matches = sum(len(o.complete_orders)
              for o in matching_engine.order_books.values())
matches / num_orders


#  Test cancels


orders = get_data(num_orders)
cancels = [CancelOrder(instrument_id=o.instrument_id,
                       order_id=o.order_id,
                       order_direction=o.order_direction)
           for o in orders]
orders = orders + cancels
random.shuffle(orders)

matching_engine = MatchingEngine()
for order in orders:
    matching_engine.add_order(order)
# matching_engine.match()

# Profile

cProfile.run("matching_engine.match()", "prof_file")
p = pstats.Stats("prof_file")
p.strip_dirs().sort_stats(-1).print_stats(10)

matches_or_cancels = sum(len(o.complete_orders)
                         for o in matching_engine.order_books.values())

cancels = sum(len([x for x in o.complete_orders if x.status == OrderStatus.cancelled])  # type: ignore
              for o in matching_engine.order_books.values())

cancels / num_orders  # type: ignore
matches_or_cancels / num_orders
