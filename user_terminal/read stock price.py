from github import Github
import sqlite3

connect_stock = sqlite3.connect( "stock_prices.db" )
curs_stock = connect_stock.cursor()


#gets the current stock price for stock A
def current_bid_price(stock):
    curs_stock.execute("SELECT bid FROM ? WHERE time = (SELECT MAX(time) FROM stock A)",(stock))####
    bid_price=curs_stock.fetchone()
    return bid_price

#gets an array of stock prices for stock A from start datetime to end date time
def bid_price_inveval(stock, start, end):
    curs_stock.execute("SELECT bid FROM ? WHERE time BETWEEN ? AND ?",(stock,start,end))#####
    bid_price_raw = curs_stock.fetchall()
    bid_price=[]
    for data in  bid_price_raw:
        temp = []  # creates 2d array per row
        for x in data:
            temp.append( x )
        bid_price.append( temp )  #3D array
    return bid_price

#gets the current stock price for stock A
def current_ask_price(stock):
    curs_stock.execute("SELECT ask FROM ? WHERE time = (SELECT MAX(time) FROM stock A)",(stock))####
    ask_price=curs_stock.fetchone()
    return ask_price

#gets an array of stock prices for stock A from start datetime to end date time
def ask_price_inveval(stock, start, end):
    curs_stock.execute("SELECT ask FROM ? WHERE time BETWEEN ? AND ?",(stock,start,end))#####
    ask_price_raw = curs_stock.fetchall()
    ask_price=[]
    for data in  ask_price_raw:
        temp = []  # creates 2d array per row
        for x in data:
            temp.append( x )
        ask_price.append( temp )  #3D array
    return ask_price
