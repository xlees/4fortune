#coding: utf-8
'''

@author: Xiang
'''

import tushare as ts
import numpy as np
import pandas as pd
from datetime import datetime
import arrow
import random
import time



def download_tick_data(cdate=arrow.now().format('YYYY-MM-DD'), days=3):
	tod = arrow.get(cdate)
	_end = tod.format('YYYY-MM-DD')
	_start = tod.replace(days=-days).format('YYYY-MM-DD')
	print 'start=%s, end=%s' % (_start,_end)
	
#	stocks = random.sample(ts.get_stock_basics().index, 5)
	stocks = ts.get_stock_basics().index
	_dates = ts.get_h_data('000001', start=_start, end=_end, index=True).index[:days]
	dates = [x.to_datetime().strftime("%Y-%m-%d") for x in _dates]
	
	print "%d stocks retrieved." % (len(stocks))
	time.sleep(5.0)
    
	def tick(tstamp):
	    date = tstamp.split(" ")[0]
	    tick_data = ts.get_tick_data(code,date=date,retry_count=10,pause=5)
	    nrows = tick_data.shape[0]
	    tick_data['date'] = pd.Series([date]*nrows)
	    
	    return tick_data
	
	def trans(ttype):
	    _ttype = ttype.decode('utf-8')
	    if _ttype == u'买盘':
	        return 2
	    elif _ttype == u'卖盘':
	        return 1
	    else:
	        return 0
	
	cols = ['date','code','time','type','price','volume','amount']
	n_avail = 0
	for code in stocks:
	    try:
	        df = map(tick, dates)
	        print 'code=', code, '. list shape:\n', df[0].head(2)
	        
	        print 'saving stock data...'
	        result = pd.concat(df)
	        result['code'] = pd.Series([code]*result.shape[0])
	        
	        # change type to digit
	        result['type'] = map(trans, result['type'])
	        
	        result[cols].to_csv("stocks/%s.csv" % (code), mode='w',header=False,index=False)
	        
	        n_avail += 1
	    except Exception as e:
	        print "stock %s failure." % (code)
	        
	    print "%s finished." % (code)
	    time.sleep(0.5)
	
	print "\n%d stocks, %d avail, %d unavailable." % (len(stocks), n_avail, len(stocks)-n_avail)

def check_if_reach_limit(code, date=datetime.now().strftime("%Y-%m-%d")):
    """
    """
    kdata = ts.get_hist_data(code,date,date,ktype='D')
    if kdata.ix[0]['p_change'] < 9.9:
        return False
    
    stock = ts.get_tick_data(code,date)[['time','price']]
    indx, = np.where(np.diff(list(reversed(stock['price'])))==0)
    
#     print "length: ", len(indx)
    
    arr = []
    beg = 0
    cur = indx[0]-1
    for i,val in enumerate(indx):
        if cur+1 == val:
            cur += 1
        else:
            if i > (beg+1):
                arr.append((indx[beg], indx[i-1]))
            beg = i
            cur = val
    arr.append((indx[beg],cur))
    mindx = np.argmax([x[1]-x[0] for x in arr])
        
    print "length of arr: ", len(arr)
        
    p = arr[mindx][0]
    print 'starting index: ', p
    print 'starting time: ', stock.ix[stock.shape[0]-p-1]['time']
    
    return stock.ix[stock.shape[0]-p-1]['time']

if __name__ == '__main__':
    print "tushare"
    tod = datetime.now().strftime("%Y-%m-%d")
    
    download_tick_data(days=5)
    
#     df = ts.get_realtime_quotes('300480')   # 实时分笔
#     curdata = df.iloc[0]
#     print len(curdata)
#     print curdata[['name','price','ask','bid']]
#     
#     print check_if_reach_limit('300382', '2015-11-12')
    
#     fc = ts.forecast_data(2015,2)
#     print fc.shape