from github import Github
import sqlite3

connect_stock = sqlite3.connect( "stock_prices.db" )
curs_stock = connect_stock.cursor()

def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
#gets the current stock price for stock A
def current_bid_price(stock):
    curs_stock.execute(f"SELECT bid FROM [{stock}] WHERE time = (SELECT MAX(time) From [{stock}] )")####
    bid_price=curs_stock.fetchone()[0]
    return bid_price

#gets an array of stock prices for stock A from start datetime to end date time
def bid_price_interval(stock, start, end):
    curs_stock.execute(f"SELECT bid FROM [{stock}] WHERE time BETWEEN [{start}] AND [{end}]",)#####
    return tuple_to_array(curs_stock.fetchall())

#gets the current stock price for stock A
def current_ask_price(stock):
    curs_stock.execute(f"SELECT ask FROM [{stock}] WHERE time = (SELECT MAX(time) FROM [{stock}] )",)####
    ask_price=curs_stock.fetchone()[0]
    return ask_price

#gets an array of stock prices for stock A from start datetime to end date time
def ask_price_interval(stock, start, end):
    curs_stock.execute(F"SELECT ask  FROM [{stock}] WHERE time BETWEEN [{start}] AND [{end}]")
    return tuple_to_array(curs_stock.fetchall())

def current_last_price(stock):
    curs_stock.execute(f"SELECT last_trade_price FROM [{stock}] WHERE time = (SELECT MAX(time) FROM [{stock}])")####
    ask_price=curs_stock.fetchone()[0]
    return ask_price

#gets an array of stock prices for stock A from start datetime to end date time
def last_price_interval(stock, start, end):
    curs_stock.execute(F"SELECT last_trade_price  FROM [{stock}] WHERE time BETWEEN [{start}] AND [{end}]")#####
    return tuple_to_array(curs_stock.fetchall())

def get_stock_names():
    return [row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

