import os
import random
import sqlite3
import time
from time import gmtime, strftime
from user_terminal.order_matching_algorithm import curs_exchange, connect_exchange
from user_terminal.read_stock_price import current_ask_price
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# for x in range(100):
#     ordernum = int(open("ordernum.txt", "r").readline())
#     curs_exchange.execute(
#         "INSERT INTO  active_orders (order_number,buy_or_sell, username, ask_bid_price_per_share,quantity, stock, time_of_execution) VALUES (?,?,?,?,?,?,?)",
#         (ordernum, "buy", "bot1", round(current_ask_price("AAPL")*(1+round(random.uniform(-2,2)/100,2)),1), round(random.uniform(10,1000),1), "AAPL", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
#
#
#     print(x)
#     connect_exchange.commit()
#     new = open("ordernum.txt", "w")
#     new.write(str(ordernum + 1))
#     new.close()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_db_path = os.path.join(BASE_DIR, "credentials.db")
connect_credentials = sqlite3.connect(cred_db_path)
curs_credentials = connect_credentials.cursor()

def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array

strat = []
loc=[]
for user in [row[0] for row in curs_credentials.execute("SELECT username From Credentials").fetchall()]:
    try:
        print(user)
        conn_user = sqlite3.connect( user+"/"+user + ".db")
        curs_user = conn_user.cursor()
        strat.append(tuple_to_array(curs_user.execute("SELECT * from strategy").fetchall()))
    except:
        pass
for x in strat:
    for y in x:
        print(y)
        try:
            if y[2]==1:
                loc.append(y[1])
        except:
            pass
print(loc)