import sqlite3
import time
from time import gmtime, strftime
from update_stock_price import main
connect_stock = sqlite3.connect( "stock_prices.db",check_same_thread=False )
curs_stock = connect_stock.cursor()
connect_stock.execute('PRAGMA journal_mode=WAL;')

connect_exchange = sqlite3.connect( "exchange.db",check_same_thread=False )
curs_exchange = connect_exchange.cursor()
connect_exchange.execute('PRAGMA journal_mode=WAL;')


def check_funds(username,buy_sell,pps,quantity):
    if buy_sell=="buy":
        conn_buyer = sqlite3.connect(username+"/"+username+".db",check_same_thread=False)
        curs_buyer = conn_buyer.cursor()
        if float(curs_buyer.execute("SELECT quantity FROM portfolio WHERE stock='cash'").fetchone()[0])<float(quantity*pps):
            print("insufficent funds",float(curs_buyer.execute("SELECT quantity FROM portfolio WHERE stock='cash'").fetchone()[0]))
            return False
        else:
            return True
    else:
        return True



def execute_order(username,buy_sell,pps,quantity,stock):
    if check_funds(username,buy_sell,pps,quantity)==True:

        ordernum=int(open("ordernum.txt","r").readline())
        print("current user:",[buy_sell,username,pps,quantity,stock])
        curs_exchange.execute("INSERT INTO  active_orders (order_number,buy_or_sell, username, ask_bid_price_per_share,quantity, stock, time_of_execution) VALUES (?,?,?,?,?,?,?)",
                                 (ordernum,buy_sell,username,pps,quantity, stock ,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        connect_exchange.commit()
        new = open("ordernum.txt", "w")
        new.write(str(ordernum + 1))
        new.close()

    else:
        return
