import multiprocessing
import os
import threading
import time
import sqlite3
import subprocess
from order_matching_algorithm import *

# Define the order matching algorithm
def order_matching_runner():
    while True:
        recheck_all()


# Function to run a bot script
def run_bot_script(file_path):
    while True:
        print(f"Running bot script: {file_path} at {time.strftime('%H:%M:%S')}")
        # Use subprocess to run the bot script
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        file_path_2 = os.path.join(BASE_DIR, file_path[14:])
        print(file_path_2)
        subprocess.run([r'C:\Users\dev26\Documents\SimulatedGame\venv\Scripts\python.exe', file_path_2])

        #exec(open(file_path_2).read())
        # Simulate staggered start

# Function to start the order matching algorithm in a separate process
def start_order_matching():
    process = multiprocessing.Process(target=order_matching_runner)
    process.start()

# Function to start all bot scripts using threading
def start_bot_scripts():
    # Connect to the database and fetch bot script file paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cred_db_path = os.path.join(BASE_DIR, "credentials.db")
    connect_credentials = sqlite3.connect(cred_db_path)
    curs_credentials = connect_credentials.cursor()

    def tuple_to_array(tuple):
        array = []
        for data in tuple:
            temp = []  # creates 2d array for all credentials
            for x in data:
                temp.append(x)
            array.append(temp)  # 3D array
        return array

    strat = []
    loc = []
    for user in [row[0] for row in curs_credentials.execute("SELECT username From Credentials").fetchall()]:
        try:
            user_db= os.path.join(BASE_DIR,user + "/" + user + ".db")
            conn_user = sqlite3.connect(user_db)
            curs_user = conn_user.cursor()
            strat.append(tuple_to_array(curs_user.execute("SELECT * from strategy").fetchall()))
        except:
            pass
    for x in strat:
        for y in x:
            try:
                if y[2] == 1:
                    loc.append(y[1])
            except:
                pass
    for a in loc:
        threading.Thread(target=run_bot_script, args=(a,), daemon=True).start()

if __name__ == "__main__":
    # Path to the database file
    # Start the order matching algorithm
    start_order_matching()

    # Start the bot scripts
    start_bot_scripts()

    # Keep the main thread alive
    while True:
        time.sleep(1)
