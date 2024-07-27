import sqlite3

from user_terminal.read_stock_price import get_stock_names

connect_stock = sqlite3.connect( "stock_prices.db" )
curs_stock = connect_stock.cursor()
connect_exchange = sqlite3.connect( "exchange.db" )
curs_exchange = connect_exchange.cursor()

def main():
    names=get_stock_names()
    for name in names:
        curs_exchange.execute(f"SELECT MAX(ask_bid_price_per_share) FROM active_orders WHERE (buy_or_sell = 'buy') AND (stock=?)",(name,))
        bid=curs_exchange.fetchone()[0]
        curs_exchange.execute(f"SELECT MIN(ask_bid_price_per_share) FROM active_orders WHERE (buy_or_sell = 'sell') AND (stock =?)",(name,))
        ask=curs_exchange.fetchone()[0]
        curs_exchange.execute(f"SELECT bid_pps,time_of_execution FROM past_orders WHERE reciept_number = (SELECT MAX(reciept_number) FROM past_orders WHERE  (stock =?)) AND  (stock =?)",(name,name))
        last=curs_exchange.fetchall()[0]
        curs_stock.execute(f"INSERT INTO [{name}] (bid,ask,last_trade_price,time) VALUES (?,?,?,?)",(bid,ask,last[0],last[1]))
    connect_stock.commit()

if __name__=="__main__":
    main()