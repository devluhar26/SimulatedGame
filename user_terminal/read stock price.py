from github import Github
import sqlite3

connect_stock = sqlite3.connect( "stock.db" )
curs_stock = connect_stock.cursor()


#gets the current stock price for stock A
def current_stockprice(stock):
    curs_stock.execute("SELECT stockprice FROM STOCK A WHERE max(time)")####
    stock_price=curs_stock.fetchone()
    return stock_price

#gets an array of stock prices for stock A from start datetime to end date time
def stockprice_inveval(stock, start, end):
    curs_stock.execute("SELECT stockprice FROM STOCK A WHERE ")#####
    stock_price_raw = curs_stock.fetchall()
    stock_price=[]
    for data in  stock_price_raw:
        temp = []  # creates 2d array per row
        for x in data:
            temp.append( x )
        stock_price.append( temp )  #3D array
    return stock_price
