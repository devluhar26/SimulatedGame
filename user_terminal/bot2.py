import time
import threading
from datetime import datetime
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
    percent_adjust=round(random.uniform(-2,2)/100,4)
    buy = 0
    sell = 0
    if choice==0:
        buy_sell="buy"
        pps=round(current_ask_price(stock)*(1-percent_adjust),2)
        buy+=1
    else:
        buy_sell="sell"
        pps=round(current_bid_price(stock)*(1+percent_adjust),2)
        sell-=1
    quantity=round(random.uniform(1, 50), 1)
    execute_order(username=username,buy_sell=buy_sell,pps=pps,quantity=quantity,stock=stock)
