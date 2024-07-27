import sqlite3
import time
from time import gmtime, strftime

connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()

def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
def execute_trade(username,buy_sell,pps,quantity,stock,trade_to_execute):
    # pps and username varies of whether buy_sell is buy or sell since if user is seller then bid price will be the one on the exchange whereas if user is buyer then bid price will be inputted by system

    if buy_sell=="buy":
        conn_buyer=sqlite3.connect(username+".db")
        curs_buyer=conn_buyer.cursor()
        conn_seller = sqlite3.connect(str(trade_to_execute[2]) + ".db")
        curs_seller = conn_seller.cursor()
        pps=pps

    if buy_sell == "sell":
        conn_seller = sqlite3.connect(username + ".db")
        curs_seller = conn_seller.cursor()
        conn_buyer = sqlite3.connect(str(trade_to_execute[2]) + ".db")
        curs_buyer = conn_buyer.cursor()
        pps=trade_to_execute[3]

    try:
        old_quantity=(curs_seller.execute("SELECT quantity FROM portfolio WHERE stock=?",(stock,)).fetchone()[0])
    except:
        old_quantity=0
    if old_quantity == quantity:
        curs_seller.execute("DELETE FROM portfolio WHERE stock=?", (stock,))
    elif old_quantity - quantity>0:
        curs_seller.execute("UPDATE portfolio SET (quantity,long_or_short)=(?,?) WHERE stock=(?)",((old_quantity-quantity),"long",stock))
    elif old_quantity - quantity>0:
        curs_seller.execute("UPDATE portfolio SET (quantity,long_or_short)=(?,?) WHERE stock=(?)",((old_quantity-quantity),"short",stock))
    old_cash=(curs_seller.execute("SELECT quantity FROM portfolio WHERE stock='cash'",).fetchone()[0])
    curs_seller.execute("UPDATE portfolio SET (quantity)=(?) WHERE stock='cash'", (old_cash+(pps * quantity),))
    ###seller done
    try:
        old_quantity_2=(curs_buyer.execute("SELECT quantity FROM portfolio WHERE stock=?",(stock,)).fetchone()[0])
    except:
        old_quantity_2=0
    if old_quantity_2 == None:
        curs_buyer.execute("INSERT INTO portfolio (stock,quantity,initial_price_per_share,long_or_short) VALUES (?,?,?,?)",(stock, quantity, pps, "long"))
    elif old_quantity_2 +quantity>0:
        curs_buyer.execute("UPDATE portfolio SET (quantity,long_or_short)=(?,?) WHERE (stock)=(?)", (old_quantity_2+quantity,"long", stock))
    elif old_quantity_2 +quantity<0:
        curs_buyer.execute("UPDATE portfolio SET (quantity,long_or_short)=(?,?) WHERE (stock)=(?)", (old_quantity_2+quantity,"short", stock))
    old_cash_2=(curs_buyer.execute("SELECT quantity FROM portfolio WHERE stock='cash'",).fetchone()[0])
    curs_buyer.execute("UPDATE portfolio SET (quantity)=(?) WHERE stock='cash'", (old_cash_2*(pps * quantity),))

    conn_buyer.commit()
    conn_seller.commit()
    connect_exchange.commit()



def quantity_adjustments(username,buy_sell,pps,quantity,stock,trade_to_execute,ordernum):
    if trade_to_execute[4]<quantity:
        recieptnum = int(open("recieptnum.txt", "r").readline())

        execute_trade(username, buy_sell, pps, trade_to_execute[4], stock, trade_to_execute)
        if buy_sell=="buy":
            curs_exchange.execute(
                "INSERT INTO past_orders (reciept_number,buyer_username,bid_pps,quantity,ask_pps,seller_username,time_of_execution) VALUES (?,?,?,?,?,?,?)",
                (recieptnum,username,pps ,trade_to_execute[4] ,trade_to_execute[3] ,trade_to_execute[2] ,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            print("1")
            print("executed order:",[recieptnum,username,pps ,trade_to_execute[4] ,trade_to_execute[3] ,trade_to_execute[2]])
        else:
            curs_exchange.execute(
                "INSERT INTO past_orders (reciept_number,buyer_username,bid_pps,quantity,ask_pps,seller_username,time_of_execution) VALUES (?,?,?,?,?,?,?)",
                (recieptnum,trade_to_execute[2],trade_to_execute[3] ,trade_to_execute[4] ,pps ,username ,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            print("2")
            print("executed order:",[recieptnum,username,pps ,trade_to_execute[4] ,trade_to_execute[3] ,trade_to_execute[2]])
        curs_exchange.execute("DELETE FROM active_orders WHERE order_number=?", ( trade_to_execute[0],))

        curs_exchange.execute("UPDATE active_orders SET (quantity)=(?)  WHERE (order_number)=(?)",(quantity-trade_to_execute[4],ordernum))
        new = open("recieptnum.txt", "w")
        new.write(str(recieptnum + 1))
        new.close()
        check_database(username, buy_sell, pps, quantity-trade_to_execute[4], stock, ordernum)


        #add sellers quantity of stock to buyers portfolio then remove sellers stock from sellers portfolio, modify buyers active order by buyer quantity- sellers quantity
    if trade_to_execute[4]>quantity:
        recieptnum = int(open("recieptnum.txt", "r").readline())
        execute_trade(username, buy_sell, pps, quantity, stock, trade_to_execute)
        if buy_sell == "buy":
            curs_exchange.execute(
                "INSERT INTO past_orders (reciept_number,buyer_username,bid_pps,quantity,ask_pps,seller_username,time_of_execution) VALUES (?,?,?,?,?,?,?)",
                (recieptnum, username, pps, quantity, trade_to_execute[3], trade_to_execute[2],
                 time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            print("3")
            print("executed order:",[recieptnum, username, pps, quantity, trade_to_execute[3], trade_to_execute[2]])
        else:
            curs_exchange.execute(
                "INSERT INTO past_orders (reciept_number,buyer_username,bid_pps,quantity,ask_pps,seller_username,time_of_execution) VALUES (?,?,?,?,?,?,?)",
                (recieptnum, trade_to_execute[2], trade_to_execute[3], quantity, pps, username,
                 time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            print("4")
            print("executed order:",[recieptnum, trade_to_execute[2], trade_to_execute[3], quantity, pps, username])
        curs_exchange.execute("DELETE FROM active_orders WHERE order_number=?", (ordernum,))

        curs_exchange.execute("UPDATE active_orders SET(quantity)=(?) WHERE (order_number)=(?)",(trade_to_execute[4]-quantity, trade_to_execute[0]))
        new = open("recieptnum.txt", "w")
        new.write(str(recieptnum + 1))
        new.close()
        check_database(trade_to_execute[2], trade_to_execute[1], trade_to_execute[3], trade_to_execute[4]-quantity, trade_to_execute[5], trade_to_execute[0])


        #add buyers quantity of stock to buyers portfolio then remove buyer from active orders and keep seller on active order with reduced quantity
    if trade_to_execute[4]==quantity:
        recieptnum = int(open("recieptnum.txt", "r").readline())

        execute_trade(username, buy_sell, pps, trade_to_execute[4], stock, trade_to_execute)

        curs_exchange.execute("DELETE FROM active_orders WHERE order_number=?", (ordernum,))
        curs_exchange.execute("DELETE FROM active_orders WHERE order_number=?", ( trade_to_execute[0],))

        if buy_sell == "buy":
            curs_exchange.execute(
                "INSERT INTO past_orders (reciept_number,buyer_username,bid_pps,quantity,ask_pps,seller_username,time_of_execution) VALUES (?,?,?,?,?,?,?)",
                (recieptnum, username, pps, trade_to_execute[4], trade_to_execute[3], trade_to_execute[2],
                 time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            print("5")

            print("executed order:",[recieptnum, username, pps, trade_to_execute[4], trade_to_execute[3], trade_to_execute[2]])
        else:
            curs_exchange.execute(
                "INSERT INTO past_orders (reciept_number,buyer_username,bid_pps,quantity,ask_pps,seller_username,time_of_execution) VALUES (?,?,?,?,?,?,?)",
                (recieptnum, trade_to_execute[2], trade_to_execute[3], trade_to_execute[4], pps, username,
                 time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            print("6")
            print("executed order:",[recieptnum, trade_to_execute[2], trade_to_execute[3], trade_to_execute[4], pps, username])
        new = open("recieptnum.txt", "w")
        new.write(str(recieptnum + 1))
        new.close()
    connect_exchange.commit()




def check_database(username,buy_sell,pps,quantity,stock,ordernum):

    if buy_sell=="buy":
        curs_exchange.execute(
            "SELECT * FROM active_orders WHERE (stock = ?) AND (username != ?) AND (ask_bid_price_per_share <= ?)  AND (buy_or_sell != ?) ORDER BY abs(ask_bid_price_per_share - ?), order_number",(stock, username,pps ,buy_sell,pps))
    if buy_sell == "sell":
        curs_exchange.execute(
            "SELECT * FROM active_orders WHERE (stock = ?) AND (username != ?) AND (ask_bid_price_per_share >= ?)  AND (buy_or_sell != ?) ORDER BY abs(ask_bid_price_per_share - ?), order_number",(stock, username, pps, buy_sell, pps))
    orders=tuple_to_array(curs_exchange.fetchall())
    print("potential stocks to buy:",orders)
    if len(orders)==0:
        print("currently no active orders to match current order")
    else:
        quantity_adjustments(username,buy_sell,pps,quantity,stock,orders[0],ordernum)

def check_funds(username,buy_sell,pps,quantity):
    if buy_sell=="buy":
        conn_buyer = sqlite3.connect(username+".db")
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
        check_database(username,buy_sell,pps,quantity,stock,ordernum)
    else:
        return
#to use
# from order_matching_algorithm import execute_order
# execute_order(...)