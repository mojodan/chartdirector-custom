#!/usr/bin/python
import cgi
import setup_env
import datetime
from FinanceChart import *
from cashflow.trading.helpers import lookup_instrument, getBarMin01, mm_in_day
from cashflow.trading.models import BarMin01

dd = cgi.FieldStorage()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day

# Locate the high and low basket instruments (custom instruments precalculated by populate_basket)
es = lookup_instrument('ES')
vb = lookup_instrument('ESH2_VB')
hb = lookup_instrument('B_H60x3')
lb = lookup_instrument('B_L60x3')

# Trading Date
if dd.has_key('day'):
    day = int(dd['day'].value)
if dd.has_key('month'):
    month = int(dd['month'].value)
if dd.has_key('year'):
    year = int(dd['year'].value)
trade_date = datetime.date(year,month,day)

# Other paraemetres
width = 1200
if dd.has_key('width'):
    width = int(dd['width'].value)
if width < 500:
    width = 1200

# Reading the instrument data for the day
bars = getBarMin01(es, trade_date)

# {'instrument', 'when', 'mm_in_day', 'open', 'high', 'low', 'close', 'volume', 'op', etc }
ts = [chartTime(d.when.year, d.when.month, d.when.day, d.when.hour, d.when.minute, 0) for d in bars]
es_open = [x.open for x in bars]
es_high = [x.high for x in bars]
es_low = [x.low for x in bars]
es_close = [x.close for x in bars]
es_vol = [x.volume for x in bars]

# Basket Data gathering
bars = getBarMin01(hb, trade_date)
hb_data = [x.close for x in bars]
bars = getBarMin01(lb, trade_date)
lb_data = [x.close for x in bars]


# Volume Breakdown Data
bars = getBarMin01(vb, trade_date)
vb_open = [0 for x in bars]
vb_high = [x.high for x in bars]
vb_low = [x.low for x in bars]
vb_close = [x.close for x in bars]


#c = FinanceChart(1024)
c = FinanceChart(2200)

# Add a title to the chart
c.addTitle("Basket Divergences - %s" % trade_date.strftime('%D (%a)'))

# Set the data into the finance chart object
c.setData(ts, es_high, es_low, es_open, es_close, es_vol, None)

# Add the main chart with 240 pixels in height
es_chart = c.addMainChart(600)

# Add HLOC symbols to the main chart, using green/red for up/down days
#c.addHLOC('0x008000', '0xcc0000')
c.addCandleStick('0x008000', '0xcc0000')

# Add a 75 pixels volume bars sub-chart to the bottom of the main chart, using
# green/red/grey for up/down/flat days
#c.addVolBars(75, '0x99ff99', '0xff9999', '0x808080')
#c.addVolIndicator(75, '0x99ff99', '0xff9999', '0x808080')

# Add the evolving high and low as line indicators to the chart
hod = [max(es_high[:i+1]) for i, v in enumerate(es_high)]
lod = [min(es_low[:i+1]) for i, v in enumerate(es_low)]
c.addLineIndicator2(es_chart, hod, '0xFF6600', 'HOD')
c.addLineIndicator2(es_chart, lod, '0xFF6600', 'LOD')

# Initial Balance High and Low
ib_high = [NoValue for x in xrange(60)] + [max(es_high[:60]) for x in xrange(390-60)]
ib_low = [NoValue for x in xrange(60)] + [min(es_low[:60]) for x in xrange(390-60)]
ll_ib_high = c.addLineIndicator2(es_chart, ib_high, '0xCC9900', 'IBH')
ll_ib_high.addCustomDataLabel(0,389,"IBH", "Arial", 8, 0x3D5AA3, 0)
ll_ib_low = c.addLineIndicator2(es_chart, ib_low, '0xCC9900', 'IBL')
#ll_ib_low = es_chart.addLineLayer2()
#ll_ib_low.addDataSet(ib_low, 0xFFFF00)
ll_ib_low.addCustomDataLabel(0,389,"IBL", "Arial", 8, 0x3D5AA3, 0)


ll_lb = es_chart.addLineLayer2()
ll_lb.addDataSet(lb_data, 0xff0000)
ll_lb.setUseYAxis2(True)
es_chart.yAxis2().setLinearScale(0, 40, 5)
ll_hb = es_chart.addLineLayer2()
ll_hb.addDataSet(hb_data, 0x3333cc)
ll_hb.setUseYAxis2(True)


# Add the volume break down layer if data is present
if len(vb_open) == 390:
    vb_chart = c.addBarIndicator(175, [], 0x000000, "Volume Breakdown")
    ll_vb = vb_chart.addCandleStickLayer(vb_high, vb_low, vb_open, vb_close, 0x008000, 0xcc0000)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))
