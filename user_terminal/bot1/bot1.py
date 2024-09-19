from order_placement import *
from uid_retriever import *
from read_stock_price import *
from numpy import random

username="bot1"
key=idnum(username)
def main2():
    names=get_stock_names()
    stock = names[0]
    choice=random.uniform(0,1)
    if choice<=(1/2):
        buy_sell="buy"
        mu = current_ask_price(stock)
        sigma = 3
        pps = random.normal(loc=mu, scale=sigma)
    else:
        buy_sell="sell"
        mu = current_bid_price(stock)
        sigma = 3
        pps = random.normal(loc=mu, scale=sigma)
    quantity = round(abs(pps-mu)*100,2)
    if quantity==0:
        quantity=100
    execute_order(username=username,buy_sell=buy_sell,pps=pps,quantity=quantity,stock=stock,key=key)

if __name__=="__main__":
    main2()