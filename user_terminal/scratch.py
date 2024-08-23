
import multiprocessing
import os
import threading
import time
import sqlite3
import subprocess
from concurrent.futures import ThreadPoolExecutor


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# cred_db_path = os.path.join(BASE_DIR, "credentials.db")
# connect_credentials = sqlite3.connect(cred_db_path,check_same_thread=False)
# curs_credentials = connect_credentials.cursor()

new = open(os.path.join(BASE_DIR,"compiler_location.txt"))
compiler_location = new.readline()



def run_bot_script(script_loc):
            print("run")
            subprocess.run([compiler_location, script_loc])

        # Simulate staggered start
def start_bot_scripts(script_loc):
    print(script_loc)
    multiprocessing.Process(target=run_bot_script,args=(str(script_loc),)).start()
def order_matching_runner():
        pass
        # process1 = multiprocessing.Process(target=recheck_all())
        # process1.start()


def start_order_matching():
    with ThreadPoolExecutor() as executor:
        while True:
            # executor.map(recheck_all(), range(10))
            # executor.map(check_incomplete(), range(1))

            time.sleep(0.1)


if __name__ == "__main__":
    # Path to the database file
    # Start the order matching algorithm
    scripts = [os.path.join(BASE_DIR, f"test{i}.py") for i in range(10)]
    for x in range(10):
        start_bot_scripts(scripts[x])
    #start_order_matching()

    # Start the bot scripts

    # Keep the main thread alive
    # while True:
    #     time.sleep(0)
