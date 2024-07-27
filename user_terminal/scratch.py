import os
import random
import sqlite3
import time
from time import gmtime, strftime
from user_terminal.order_matching_algorithm import curs_exchange, connect_exchange

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for x in range(100):
    ordernum = int(open("ordernum.txt", "r").readline())
    curs_exchange.execute(
        "INSERT INTO  active_orders (order_number,buy_or_sell, username, ask_bid_price_per_share,quantity, stock, time_of_execution) VALUES (?,?,?,?,?,?,?)",
        (ordernum, "sell", "dev", round(random.uniform(60,120),1), round(random.uniform(10,1000),1), "AAPL", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))


    print(x)
    connect_exchange.commit()
    new = open("ordernum.txt", "w")
    new.write(str(ordernum + 1))
    new.close()