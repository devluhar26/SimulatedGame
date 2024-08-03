import time
import threading
from datetime import datetime

import numpy as np

from order_matching_algorithm import *
from read_stock_price import *
import random
from multiprocessing import Process

connect_exchange = sqlite3.connect( "exchange.db",check_same_thread=False )
curs_exchange = connect_exchange.cursor()
curs_exchange.execute('PRAGMA journal_mode=WAL;')
import bot2
import bot4
import bot5
def main1(username):
    names=get_stock_names()
    stock = names[random.randint(0, len(names) - 1)]
    choice=random.randint(0,1)
    percent_adjust = 0
    percent_adjust = round(np.random.normal(loc=0.003, scale=0.0005), 4)
    buy = 0
    sell = 0
    if choice==0:
        buy_sell="buy"
        pps=round(current_last_price(stock)*(1-percent_adjust),2)
        buy+=1
    else:
        buy_sell="sell"
        pps=round(current_last_price(stock)*(1+percent_adjust),2)
        sell-=1
    quantity = round(1500 * (1 - percent_adjust), 1)
    execute_order(username=username,buy_sell=buy_sell,pps=pps,quantity=quantity,stock=stock)


def check_incomplete(username):
    orders=tuple_to_array(curs_exchange.execute("SELECT * FROM active_orders WHERE (username)=(?)",(username,)).fetchall())
    for order in orders:
        difference=datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),"%Y-%m-%d %H:%M:%S")- datetime.strptime(order[6], "%Y-%m-%d %H:%M:%S")
        if difference.seconds>=100:
            #cancel_order(order[0])
            if order[1]=="buy":
                try:
                    new_price = curs_exchange.execute(
                        "SELECT MIN(ask_bid_price_per_share) FROM active_orders WHERE  (stock =?) AND (buy_or_sell='sell') AND (username!=?)",
                        (order[5], order[2])).fetchone()
                    cancel_order( order[0])

                    execute_order(username=username, buy_sell=order[1], pps=new_price[0], quantity=order[4],
                                      stock=order[5])

                except:
                    pass

                #recheck_all()
            if order[1]=="sell":
                try:
                    new_price = curs_exchange.execute(
                        "SELECT MAX(ask_bid_price_per_share) FROM active_orders WHERE  (stock =?) AND (buy_or_sell='buy') AND (username!=?)",
                        (order[5], order[2])).fetchone()
                    cancel_order( order[0])

                    execute_order(username=username, buy_sell=order[1], pps=new_price[0], quantity=order[4], stock=order[5])
                except:
                    pass

                #recheck_all()
        # if (difference.seconds)>=500:
        #     cancel_order(order[0])
        connect_exchange.commit()
    print("READJUSTED PRICES")
if __name__=="__main__":
    while True:
        lock=threading.Lock()
        threading.Thread(target=main1("bot1")).start()
        threading.Thread(target=main1("dev")).start()
        # check_incomplete("dev")
        # check_incomplete("bot1")
        # threading.Thread(target=bot2.main2("bot1")).start()
        # threading.Thread(target=bot2.main2("dev")).start()
        # threading.Thread(target=bot5.main5("bot1")).start()
        # threading.Thread(target=bot5.main5("dev")).start()
        # threading.Thread(target=bot5.main5("bot1")).start()
        # threading.Thread(target=bot5.main5("dev")).start()
        # threading.Thread(target=bot5.main5("bot1")).start()
        # threading.Thread(target=bot5.main5("dev")).start()
        # threading.Thread(target=bot5.main5("bot1")).start()
        # threading.Thread(target=bot5.main5("dev")).start()


