from python.src.trades import Trade
import numpy as np
import pytest


def test_trade_init():
    trade = Trade(datetime=np.datetime64("2020-01-01"), price=10, quantity=10)
    pass
