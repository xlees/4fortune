#coding: utf-8

from models import *
import tushare as ts
import sqlalchemy, sqlalchemy.orm
from sqlalchemy.orm import sessionmaker,scoped_session
from django.conf import settings
from models import *
import logging,arrow


logger = logging.getLogger('django')
logger.info("starting '"+__file__+"' ...")

engine = sqlalchemy.create_engine('sqlite:///%s/dbase/common.sqlite3' % (settings.BASE_DIR),echo=False)
Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

# service 层
def selectStocks():
	pass


def getStockInfo(*args):
	if len(args) == 0:
		return []
	else:
		sess = Session()
		result = sess.query(StockInfo).filter(StockInfo.code.in_(args)).all()
		if len(result) == 0:
			logger.warn("No stock found, fetching from internet...")

			allStocks = ts.get_stock_basics()
			for indx, row in allStocks.iterrows():
				stock = StockInfo(indx,row['name'])
				sess.merge(stock)
			sess.commit()
		sess.close()

		return result