import sqlite3
def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
conn_stock = sqlite3.connect("stock_prices.db")
curs_stock = conn_stock.cursor()
# tuple_to_array(, stock_name)
print(*[row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])