import time
import threading
from datetime import datetime

import numpy as np

from order_placement import *

from read_stock_price import *
from numpy import random
connect_exchange = sqlite3.connect( "exchange.db",check_same_thread=False )
curs_exchange = connect_exchange.cursor()
connect_exchange.execute('PRAGMA journal_mode=WAL;')

def main2(username):
    names=get_stock_names()
    for stock in names:
        mu = current_ask_price(stock)
        execute_order(username=username,buy_sell="sell",pps=mu,quantity=1000,stock=stock)
if __name__=="__main__":
        main2("admin")
