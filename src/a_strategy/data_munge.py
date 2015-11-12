#coding: utf-8
'''
Created on 2015��11��12��

@author: Xiang
'''

import tushare as ts
from datetime import datetime


def check_if_reach_limit(code, date=datetime.now().strftime("%Y-%m-%d")):
    """
    """
    kdata = ts.get_hist_data(code,date,date,ktype='D')
    if kdata.ix[0]['p_change'] < 9.9:
        return False
    
    stock = ts.get_tick_data(code,date)
    price = stock['price']
    # 查找涨停区间
    
    
    return True

if __name__ == '__main__':
    print "tushare"
    tod = datetime.now().strftime("%Y-%m-%d")
    
    df = ts.get_realtime_quotes('300212')   # 实时分笔
    curdata = df.iloc[0]
    print len(curdata)
    print curdata[['name','price','ask','bid']]
    
    print check_if_reach_limit('300212', '2015-11-09')
    
#     fc = ts.forecast_data(2015,2)
#     print fc.shape