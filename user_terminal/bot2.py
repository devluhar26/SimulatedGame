import time
import threading
from datetime import datetime

import numpy as np

from order_matching_algorithm import *

from read_stock_price import *
import random
connect_exchange = sqlite3.connect( "exchange.db",check_same_thread=False )
curs_exchange = connect_exchange.cursor()
connect_exchange.execute('PRAGMA journal_mode=WAL;')

def main2(username):
    names=get_stock_names()
    stock = names[random.randint(0, len(names) - 1)]
    choice=random.randint(0,1)
    percent_adjust = abs(np.random.normal(loc=0, scale=0.01))  # Mean 0, Std dev 1%
    if choice==0:
        buy_sell="buy"
        pps = round(current_ask_price(stock) * (1 - percent_adjust), 2)
        quantity = int((pps - 90) * 2)
        if quantity < 1:
            quantity = 1
    else:
        buy_sell="sell"
        pps=round(current_bid_price(stock)*(1+percent_adjust),2)
        quantity = int((200 - pps) * 2)
    execute_order(username=username,buy_sell=buy_sell,pps=pps,quantity=quantity,stock=stock)
