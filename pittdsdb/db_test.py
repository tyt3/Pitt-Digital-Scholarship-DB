import os
import mysql.connector
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

INFSCI2710_MyDatabase = mysql.connector.connect(
    host = os.environ.get("HOST"),
    user = os.environ.get("USER"),
    passwd = os.environ.get("PASSWORD"),
    database = os.environ.get("DATABASE")
)

my_cursor = INFSCI2710_MyDatabase.cursor()

my_cursor.execute("SELECT * FROM person")

records = my_cursor.fetchall()

for row in records:
    print(row)
