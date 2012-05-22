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
trade_date = datetime.date(2012,5,17)

# Reading the instrument data for the day
bars = getBarMin01(es, trade_date)

# {'instrument', 'when', 'mm_in_day', 'open', 'high', 'low', 'close', 'volume', 'op', etc }
ts = [chartTime(d.when.year, d.when.month, d.when.day, d.when.hour, d.when.minute, 0) for d in bars]
es_open = [x.open for x in bars]
es_high = [x.high for x in bars]
es_low = [x.low for x in bars]
es_close = [x.close for x in bars]
es_vol = [x.volume for x in bars]


c = FinanceChart(1024)

# Add a title to the chart
c.addTitle("Basket Divergences")

# Set the data into the finance chart object
c.setData(ts, es_high, es_low, es_open, es_close, es_vol, None)

# Add the main chart with 240 pixels in height
es_chart = c.addMainChart(600)

# Add HLOC symbols to the main chart, using green/red for up/down days
c.addHLOC('0x008000', '0xcc0000')

# Add a 75 pixels volume bars sub-chart to the bottom of the main chart, using
# green/red/grey for up/down/flat days
c.addVolBars(75, '0x99ff99', '0xff9999', '0x808080')

# Add the evolving high and low as line indicators to the chart
hod = [max(es_high[:i+1]) for i, v in enumerate(es_high)]
lod = [min(es_low[:i+1]) for i, v in enumerate(es_low)]
c.addLineIndicator2(es_chart, hod, '0x008000', 'HOD')
c.addLineIndicator2(es_chart, lod, '0x008000', 'LOD')

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))
