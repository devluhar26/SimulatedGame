import sqlite3
import time
from time import gmtime, strftime

connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()


def execute_order(username,buy_sell,pps,quantity,stock):
    ordernum=int(open("ordernum.txt","r").readline())
    curs_exchange.execute("INSERT INTO  active_orders (order_number,buy_or_sell, username, ask_bid_price_per_share,quantity, stock, time_of_execution) VALUES (?,?,?,?,?,?,?)",
                             (ordernum,username,buy_sell,pps,quantity, stock ,time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
    #adjust[
    connect_exchange.commit()
    new = open("ordernum.txt", "w")
    new.write(str(ordernum + 1))
    new.close()
    #check_database(username,buy_sell,pps,quantity,stock)
execute_order("dev","sell","105","10","AAPL")

# def check_database(username,buy_sell,pps,quantity,stock):
#     if buy_sell=="buy":
#         curs_exchange("SELECT * FROM active orders WHERE (stock==stock) and (username!=username) and  (ask bid price per share<=pps) and quantity>=quantity ORDERBY and min(abs(ask bid price per share-pps)) min(order number) (?,?)"(stock,username))
#         if curs_exchange.fetchall()==None:
#             return
#         else:
#             trade_to_execute=curs_exchange.fetchall()[0]
#             #now the quantity algorithm needs to be sorted
#             #fetch quantity from the trade extracted and apply things in flowchart
#
#
# def quantity_adjustments(username,buy_sell,pps,quantity,stock,trade_to_execute):
#     if buy_sell=="buy":
#         if trade_to_execute[4]<quantity:
#             #add sellers quantity of stock to buyers portfolio then remove sellers stock from sellers portfolio, modify buyers active order by buyer quantity- sellers quantity
#             pass
#         elif trade_to_execute[4]>quantity:
#             #add buyers quantity of stock to buyers portfolio then remove buyer from active orders and keep seller on active order with reduced quantity
#             pass
#         else:
#            pass
