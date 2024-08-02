from read_stock_price import *
import random
from order_matching_algorithm import *

connect_exchange = sqlite3.connect( "exchange.db",check_same_thread=False )
curs_exchange = connect_exchange.cursor()
connect_exchange.execute('PRAGMA journal_mode=WAL;')

def main5(username):
    names=get_stock_names()
    stock = names[random.randint(0, len(names) - 1)]
    percent_adjust=round(random.uniform(10,20)/100,4)
    buy_sell="buy"
    pps=round(current_ask_price(stock)*(1+percent_adjust),2)
    quantity=round(random.uniform(1, 50), 1)
    execute_order(username=username,buy_sell=buy_sell,pps=pps,quantity=quantity,stock=stock)
