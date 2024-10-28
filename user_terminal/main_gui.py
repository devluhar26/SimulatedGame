import math
import os
import random
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from nicegui import ui
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from io import BytesIO
from PIL import Image

from matplotlib import pyplot as plt
from nicegui import ui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

stock_db_path = os.path.join(BASE_DIR, "stock_prices.db")
conn_stock = sqlite3.connect(stock_db_path,check_same_thread=False)
curs_stock = conn_stock.cursor()
exchange_db_path = os.path.join(BASE_DIR, "exchange.db")
connect_exchange = sqlite3.connect( exchange_db_path,check_same_thread=False)
curs_exchange = connect_exchange.cursor()

def generate_graph(ax):
    selected_stock = "AAPL"
    ax.clear()

    try:
        bid_prices = [row[3] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='buy' ORDER BY ask_bid_price_per_share DESC").fetchall()]
        ask_prices = [row[3] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='sell' ORDER BY ask_bid_price_per_share ASC").fetchall()]
        bid_volumes = [row[4] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='buy' ORDER BY ask_bid_price_per_share DESC").fetchall()]
        ask_volumes = [row[4] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='sell' ORDER BY ask_bid_price_per_share ASC").fetchall()]
    except sqlite3.Error as e:
        pass

    # Plot the bid data
    ax.fill_between(bid_prices, bid_volumes, color='green', alpha=0.5, step='post', label='Bid')

    # Plot the ask data
    ax.fill_between(ask_prices, ask_volumes, color='red', alpha=0.5, step='post', label='Ask')

    # Formatting the plot
    ax.set_xlabel('Price')
    ax.set_ylabel('Volume')
    ax.set_title(f'Bid-Ask Spread for {selected_stock}')
    ax.legend()
    ax.grid(True)

@ui.page('/', dark=False)
def main():
    with ui.left_drawer(top_corner=True, bottom_corner=True):
        ui.label('LEFT DRAWER')

        with ui.tabs().props('vertical switch-indicator swipeable').classes('w-full') as tabs:
            one = ui.tab('Overview')
            two = ui.tab('add strategy')

    with (ui.tab_panels(tabs, value=one).classes('w-full')):
        with ui.tab_panel(one):
            with ui.tabs().classes('w-full') as inner_tabs:
                inner_one = ui.tab('Overview')
                inner_two = ui.tab('modify strategy')
            with ui.tab_panels(inner_tabs, value=inner_one).classes('w-full'):
                with ui.tab_panel(inner_one):

                    ui.label('First tab')

                    ui.label('Real-Time Ask-Bid Spread')

                    # Create the figure and axis
                    fig, ax = plt.subplots()

                    # Generate the initial graph
                    generate_graph(ax)
                    plot_container = ui.image(fig.canvas.tostring_rgb(), format='jpeg').style('width: 50%;')

                    label = ui.label()
                    stock="AAPL"
                    bidprice = [row[0] for row in curs_stock.execute(f"SELECT bid FROM [{stock}]").fetchall()]
                    askprice = [row[0] for row in curs_stock.execute(f"SELECT ask FROM [{stock}]").fetchall()]
                    price = [row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()]
                    time = [row[0] for row in curs_stock.execute(f"SELECT time FROM [{stock}]").fetchall()]

                    # Create a NiceGUI app

                    # Create an ECharts component with NiceGUI
                    echart=ui.echart({'title': {'text': 'Stock Prices'},
                                      'tooltip': {'trigger': 'axis'},
                                      'legend': {'data': ['Bid Price', 'Ask Price', 'Price']},
                                      'xAxis': {'type': 'category','data': time},
                                      'yAxis': {'type': 'value'},
                                      'series': [{'name': 'Bid Price','type': 'line','data': bidprice},
                                                 {'name': 'Ask Price','type': 'line','data': askprice},
                                                 {'name': 'Price','type': 'line','data': price}]})
                    echart.style("width: 1800px; height: 1600px;")
                    def update():
                        bidprice.append([row[0] for row in curs_stock.execute(f"SELECT bid FROM [{stock}]").fetchall()][-1])
                        askprice.append([row[0] for row in curs_stock.execute(f"SELECT ask FROM [{stock}]").fetchall()][-1])
                        price.append([row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()][-1])
                        time.append([row[0] for row in curs_stock.execute(f"SELECT time FROM [{stock}]").fetchall()][-1])

                        echart.update()
                    def check_update():
                        if [row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()][-1]!=price[-1]:
                            ui.timer(0.1, lambda: update())
                        else:
                            return
                    def update_askbidspread():
                        generate_graph(ax)
                        fig.canvas.draw()
                        plot_container.source = fig.canvas.tostring_rgb()


                    ui.timer(0.1, lambda: check_update())
                    ui.timer(0.001, lambda: label.set_text(f'{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}'))
                with ui.tab_panel(inner_two):
                    ui.label("second page")

        with ui.tab_panel(two):
            ui.label('Second tab')
            editor = ui.codemirror('print("Edit me!")', language='Python').classes('h-32')

            ui.link('Visit dark page', dark_page)


@ui.page('/dark_page', dark=True)
def dark_page():
    ui.label("new")





# Run NiceGUI on a different port
if __name__ in {"__main__", "__mp_main__"}:

    ui.run(host='0.0.0.0', port=8080)
