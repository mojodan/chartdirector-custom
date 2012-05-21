#!/usr/bin/python
import setup_env
import datetime
from FinanceChart import *
from cashflow.trading.helpers import lookup_instrument, getBarMin01, mm_in_day
from cashflow.trading.models import BarMin01


# Locate the high and low basket instruments (custom instruments precalculated by populate_basket)
es = lookup_instrument('ES')
hb = lookup_instrument('B_H60x3')
lb = lookup_instrument('B_L60x3')

# Trading Date
trade_date = datetime.date(20012,5,17)

# Reading the instrument data for the day
bars = getBarMin01(es, trade_date)

# {'instrument', 'when', 'mm_in_day', 'open', 'high', 'low', 'close', 'volume', 'op', etc }