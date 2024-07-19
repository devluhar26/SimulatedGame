import sqlite3
import time
from time import gmtime, strftime

connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()


def execute_order(username,buy_sell,pps,quantity,stock):
    ordernum=int(open("ordernum.txt","r").readline())
    curs_exchange.execute("INSERT INTO  active orders (order number,buy or sell, username, ask bid price per share,quantity, stock, time of execution) VALUES (?,?,?,?,?,?,?)",
                             (ordernum,username,buy_sell,pps,quantity, stock ,time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())))

    new = open("ordernum.txt", "w")
    new.write(str(ordernum + 1))
    new.close()
    check_database(username,buy_sell,pps,quantity,stock)

def check_database(username,buy_sell,pps,quantity,stock):
    curs_exchange("SELECT * FROM active orders WHERE (stock==stock) and (username!=username) and (buy or sell!= buy_sell) and  (ask bid price per share<=pps) and quantity>=quantity ORDERBY and min(abs(ask bid price per share-pps)) min(order number) (?,?)"(stock,username))
    if curs_exchange.fetchall()==None:
        return
    else:
        trade_to_execute=curs_exchange.fetchall()[0]


