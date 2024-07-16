import sqlite3
import time
connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()


def execute_order(username,buy_sell,pps,quantity,stock):

    ordernum=int(open("ordernum.txt","r").readline())
    new=open("ordernum.txt", "w")
    new.write(str(ordernum+1))
    new.close()

    #curs_exchange.execute("INSERT INTO  active orders (order number,buy or sell, username, ask bid price per share,quantity, stock, time of execution) VALUES (?,?,?,?,?,?,?)",
    #                         (username, password))
execute_order(1,1,1,1,1)