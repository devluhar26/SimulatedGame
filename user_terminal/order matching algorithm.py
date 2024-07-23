import sqlite3
import time
from time import gmtime, strftime

connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()

def tuple_to_array(tuple, array):
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
def execute_trade(username,buy_sell,pps,quantity,stock,trade_to_execute):
    if buy_sell=="buy":
        conn_buyer=sqlite3.connect(username+".db")
        curs_buyer=conn_buyer.cursor()

        conn_seller = sqlite3.connect(trade_to_execute[2] + ".db")
        curs_seller = conn_seller.cursor()

        if curs_seller.execute("SELECT quantity WHERE stock=?",(stock,)).fetchone()[0]==quantity:
            curs_seller.execute("DELETE FROM portfolio WHERE stock=?",(stock,))
        else:
            curs_seller.execute("UPDATE portfolio SET quantity=quantity-? WHERE (stock)=(?)", (quantity, stock))

        curs_seller.execute("UPDATE portfolio SET quantity=quantity+? WHERE stock=cash",(pps*quantity,))


        if curs_buyer.execute("SELECT quantity WHERE stock=?",(stock,)).fetchone()==None:
            curs_buyer.execute("INSERT INTO portfolio (stock,quantity,initial_price_per_share,long_or_short) VALUES (?,?,?,?)",(stock,quantity,pps,"long"))
        else:
            curs_buyer.execute("UPDATE portfolio SET quantity=quantity+? WHERE (stock)=(?)", (quantity, stock))

        curs_buyer.execute("UPDATE portfolio SET quantity=quantity-? WHERE stock=cash",(pps*quantity,))
    if buy_sell == "sell":
        conn_seller = sqlite3.connect(username + ".db")
        curs_seller = conn_buyer.cursor()

        conn_buyer = sqlite3.connect(trade_to_execute[2] + ".db")
        curs_buyer = conn_buyer.cursor()

        if curs_seller.execute("SELECT quantity WHERE stock=?",(stock,)).fetchone()[0] == quantity:
            curs_seller.execute("DELETE FROM portfolio WHERE stock=?", (stock,))
        else:
            curs_seller.execute("UPDATE portfolio SET quantity=quantity-? WHERE (stock)=(?)", (quantity, stock))

        curs_seller.execute("UPDATE portfolio SET quantity=quantity+? WHERE stock=cash", (pps * quantity,))

        if curs_buyer.execute("SELECT quantity WHERE stock=?",(stock,)).fetchone() == None:
            curs_buyer.execute(
                "INSERT INTO portfolio (stock,quantity,initial_price_per_share,long_or_short) VALUES (?,?,?,?)",
                (stock, quantity, pps, "short"))
        else:
            curs_buyer.execute("UPDATE portfolio SET quantity=quantity+? WHERE (stock)=(?)", (quantity, stock))

        curs_buyer.execute("UPDATE portfolio SET quantity=quantity-? WHERE stock=cash", (pps * quantity,))

conn_buyer=sqlite3.connect("bob.db")
curs_buyer=conn_buyer.cursor()

def quantity_adjustments(username,buy_sell,pps,quantity,stock,trade_to_execute):
    if buy_sell=="buy":
        if trade_to_execute[4]<quantity:
            #add sellers quantity of stock to buyers portfolio then remove sellers stock from sellers portfolio, modify buyers active order by buyer quantity- sellers quantity
            pass
        elif trade_to_execute[4]>quantity:
            #add buyers quantity of stock to buyers portfolio then remove buyer from active orders and keep seller on active order with reduced quantity
            pass
        else:
           pass
    if buy_sell=="sell":
        if trade_to_execute[4]<quantity:
            #add sellers quantity of stock to buyers portfolio then remove sellers stock from sellers portfolio, modify buyers active order by buyer quantity- sellers quantity
            pass
        elif trade_to_execute[4]>quantity:
            #add buyers quantity of stock to buyers portfolio then remove buyer from active orders and keep seller on active order with reduced quantity
            pass
        else:
           pass

def check_database(username,buy_sell,pps,quantity,stock):
    if buy_sell=="buy":
        curs_exchange.execute(
            "SELECT * FROM active_orders WHERE (stock = ?) AND (username != ?) AND (ask_bid_price_per_share <= ?)  AND (buy_or_sell != ?) ORDER BY abs(ask_bid_price_per_share - ?), order_number",(stock, username,pps ,buy_sell,pps))
    if buy_sell == "sell":
        curs_exchange.execute(
            "SELECT * FROM active_orders WHERE (stock = ?) AND (username != ?) AND (ask_bid_price_per_share >= ?)  AND (buy_or_sell != ?) ORDER BY abs(ask_bid_price_per_share - ?), order_number",(stock, username, pps, buy_sell, pps))

    orders=[]
    if curs_exchange.fetchall()==None:
         return
    tuple_to_array(curs_exchange.fetchall(),orders)
    print(orders)
    #quantity_adjustments(orders)

def check_funds():
    pass

def execute_order(username,buy_sell,pps,quantity,stock):
    ordernum=int(open("ordernum.txt","r").readline())
    curs_exchange.execute("INSERT INTO  active_orders (order_number,buy_or_sell, username, ask_bid_price_per_share,quantity, stock, time_of_execution) VALUES (?,?,?,?,?,?,?)",
                             (ordernum,buy_sell,username,pps,quantity, stock ,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    #adjust[
    connect_exchange.commit()
    new = open("ordernum.txt", "w")
    new.write(str(ordernum + 1))
    new.close()
    check_database(username,buy_sell,pps,quantity,stock)
execute_order("james","buy","113","11","AAPL")


