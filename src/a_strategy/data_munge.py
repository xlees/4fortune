#coding: utf-8
'''
Created on 2015��11��12��

@author: Xiang
'''

import tushare as ts
import numpy as np
from datetime import datetime


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
    
    return True

if __name__ == '__main__':
    print "tushare"
    tod = datetime.now().strftime("%Y-%m-%d")
    
    df = ts.get_realtime_quotes('300480')   # 实时分笔
    curdata = df.iloc[0]
    print len(curdata)
    print curdata[['name','price','ask','bid']]
    
    print check_if_reach_limit('300382', '2015-11-12')
    
#     fc = ts.forecast_data(2015,2)
#     print fc.shape