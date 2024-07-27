from order_matching_algorithm import execute_order
from read_stock_price import *
import random
def main(username):
    names=get_stock_names()
    stock = names[random.randint(0, len(names) - 1)]

    choice=random.randint(0,1)
    percent_adjust=round(random.uniform(-2,2),2)/100
    if choice==0:
        buy_sell="buy"
        pps=current_bid_price(stock)*(1+percent_adjust)
        print("1a")
    else:
        buy_sell="sell"
        pps=current_ask_price(stock)*(1+percent_adjust)
        print("1b")
    quantity=round(random.uniform(0.1, 0.5), 3)
    print(pps*quantity)
    execute_order(username=username,buy_sell=buy_sell,pps=round(pps,2),quantity=quantity,stock="AAPL")

if __name__=="__main__":
    main("bot1")