from python.src.orders import LimitOrder
from python.src.orders import MarketOrder
from python.src.enums import OrderDirection
from python.src.matching_engine import MatchingEngine
import random
import cProfile
import pstats


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
    return output


orders = get_data(100000)
matching_engine = MatchingEngine()
for order in orders:
    matching_engine.add_order(order)
# matching_engine.match()
cProfile.run("matching_engine.match()", "prof_file")
p = pstats.Stats("prof_file")
p.strip_dirs().sort_stats(-1).print_stats()
