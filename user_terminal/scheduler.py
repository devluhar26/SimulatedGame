import multiprocessing
import os
import threading
import time
import sqlite3
import subprocess
from order_matching_algorithm import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_db_path = os.path.join(BASE_DIR, "credentials.db")
connect_credentials = sqlite3.connect(cred_db_path,check_same_thread=False)
curs_credentials = connect_credentials.cursor()

new = open("user_terminal/compiler_location.txt")
compiler_location = new.readline()


def tuple_to_array(tuple):
    array = []
    for data in tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append(x)
        array.append(temp)  # 3D array
    return array
# Define the order matching algorithm



# Function to run a bot script
def run_bot_script():
    while True:
        all_strat = []
        all_locations = []
        for user in [row[0] for row in curs_credentials.execute("SELECT username From Credentials").fetchall()]:
            try:
                user_db = os.path.join(BASE_DIR, user + "/" + user + ".db")
                conn_user = sqlite3.connect(user_db)
                curs_user = conn_user.cursor()
                all_strat.append(tuple_to_array(curs_user.execute("SELECT * FROM strategy WHERE on_off=1").fetchall()))
            except:
                pass
        for strat_per_user in all_strat:
            for individual_strat in strat_per_user:
                try:
                    if individual_strat[2] == 1:
                        all_locations.append(individual_strat[1])
                except:
                    pass
        #print(all_locations)
        for file_path in all_locations:
            file_path_2 = os.path.join(BASE_DIR, file_path[14:])
            subprocess.run([compiler_location, file_path_2])

        # Simulate staggered start
def start_bot_scripts():
    # Connect to the database and fetch bot script file paths
    print("running bot script")

    threading.Thread(target=run_bot_script, daemon=True).start()

def order_matching_runner():
    while True:
        print("rechecking")
        process = multiprocessing.Process(target=recheck_all())
        process.start()
        #time.sleep(1)

# Function to start the order matching algorithm in a separate process
def start_order_matching():
    threading.Thread(target=order_matching_runner, daemon=True).start()


# Function to start all bot scripts using threading

if __name__ == "__main__":
    # Path to the database file
    # Start the order matching algorithm
    start_order_matching()

    # Start the bot scripts
    start_bot_scripts()

    # Keep the main thread alive
    while True:
        time.sleep(1)
