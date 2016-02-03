#coding: utf-8

import sys,os,time
reload(sys).setdefaultencoding('utf-8')

import pandas as pd
import tushare as ts
import numpy as np
import arrow
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick
from matplotlib.dates import num2date,date2num
from matplotlib.dates import AutoDateLocator, DateFormatter

pd.options.mode.chained_assignment = None  # default='warn'


def draw(code,x,y,markers=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x1 = [i for (i,e) in enumerate(x)]
    # x1 = [e[0].to_datetime() for e in tseries if e[2]==1]       # dates
    # y1 = [e[1] for e in tseries if e[2]==1]

    # ax.set_xticks(dates) # Tickmark + label at every plotted point
    # ax.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
    ax.plot(x1,y, ls='-', marker='o',markersize=6)

    # x2 = [e[0].to_datetime() for e in tseries if e[2]==-1]      # dates
    # y2 = [e[1] for e in tseries if e[2]==-1]
    # ax.plot_date(date2num(x2),y2, ls='-', marker='o',markersize=5,color='red')

    # # 全部
    # x = [e[0].to_datetime() for e in tseries]       # dates
    # y = [e[1] for e in tseries]
    # ax.plot_date(date2num(x),y, ls='--', marker='o',markersize=1,color='gray')

    # fig.autofmt_xdate(rotation=45)
    # fig.tight_layout()

    plt.savefig("%s.png"%(code))
#
def mean_regression(code='300212',start='2015-01-01',end=arrow.now().format('YYYY-MM-DD'),
                    ma=10, upper=2.0, lower=-2.0, eps=0.2):
    """
        eps: 相交时的误差
    """
    print 'fetching data of %s...' % (code)
    data = ts.get_hist_data(code,start,end)
    price = data[['close']]
    price.sort_index(inplace=True)

    #
    price['mean'] = pd.rolling_mean(price['close'],ma)
    price['std'] = pd.rolling_std(price['close'],ma)
    price['zscore'] = (price['close']-price['mean']) / price['std']

    print price.tail()

    buy_point = price[(price['zscore']<lower)]
    buy_point['dtype'] = 'B' #pd.Series([0]*buy_point.shape[0])

    sell_point = price[(np.abs(price['zscore']))<eps]
    sell_point['dtype'] = 'S' #pd.Series([1]*sell_point.shape[0])

    # print "typeof: ", buy_point.head()

    # merge
    merged = pd.concat([buy_point,sell_point],axis=0)
    merged.sort_index(inplace=True)

    # save
    fname = 'signal.csv'
    with open(fname,'w') as f:
        merged.to_csv(fname)

    # plot
    x = list(merged.index)
    y = list(merged['close'])
    draw(code,x,y)

if __name__ == '__main__':
    mean_regression(ma=15)
