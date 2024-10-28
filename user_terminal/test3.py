# nicegui_app.py
from nicegui import ui
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
# Define your chart
stock = "AMZN"
bidprice = [row[0] for row in curs_stock.execute(f"SELECT bid FROM [{stock}]").fetchall()]
askprice = [row[0] for row in curs_stock.execute(f"SELECT ask FROM [{stock}]").fetchall()]
price = [row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()]
time = [row[0] for row in curs_stock.execute(f"SELECT time FROM [{stock}]").fetchall()]

# Create a NiceGUI app

# Create an ECharts component with NiceGUI
echart = ui.echart({'title': {'text': 'Stock Prices', 'textStyle': {'color': '#FFFFFF'}},
                    'tooltip': {'trigger': 'axis'},
                    'legend': {'data': ['Bid Price', 'Ask Price', 'Price'], 'textStyle': {'color': '#FFFFFF'}},
                    'xAxis': {'type': 'category', 'data': time},
                    'yAxis': {'type': 'value'},
                    'series': [{'name': 'Bid Price', 'type': 'line', 'data': bidprice,'lineStyle': {'color': "#ffffff"},'itemStyle': {'color': "#ffffff"}},
                               {'name': 'Ask Price', 'type': 'line', 'data': askprice,'lineStyle': {'color': "#000000"},'itemStyle': {'color': "#000000"}},
                               {'name': 'Price', 'type': 'line', 'data': price,'lineStyle': {'color': "#c4a466"},'itemStyle': {'color': "#c4a466"}}]})
echart.style("width: 1500px; height: 600px;")

def update():
    bidprice.append([row[0] for row in curs_stock.execute(f"SELECT bid FROM [{stock}]").fetchall()][-1])
    askprice.append([row[0] for row in curs_stock.execute(f"SELECT ask FROM [{stock}]").fetchall()][-1])
    price.append([row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()][-1])
    time.append([row[0] for row in curs_stock.execute(f"SELECT time FROM [{stock}]").fetchall()][-1])

    echart.update()


def check_update():
    if [row[0] for row in curs_stock.execute(f"SELECT last_trade_price FROM [{stock}]").fetchall()][-1] != price[-1]:
        ui.timer(0.1, lambda: update())
    else:
        return
ui.timer(0.1, lambda: check_update())

# Start the NiceGUI server
# Run NiceGUI on a different port
if __name__ in {"__main__", "__mp_main__"}:

    ui.run(host='0.0.0.0', port=8083,show=False)