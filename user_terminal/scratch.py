import os
import sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

user_db_path = os.path.join(BASE_DIR, "bob" + ".db")
connect_user = sqlite3.connect(user_db_path)
curs_user = connect_user.cursor()

print(str(curs_user.execute("SELECT strategy_location FROM strategy WHERE strategy_name=?",("dsftryr",)).fetchone()[0]))
print(open(os.path.join(BASE_DIR,str(curs_user.execute("SELECT strategy_location FROM strategy WHERE strategy_name=?",("dsftryr",)).fetchone()[0])),"r").read())