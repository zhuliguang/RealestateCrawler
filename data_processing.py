'''
Description: Realestate data processing
Author: Nan Li
Contact: linan.lqq0@gmail.com
'''

# import packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import errorcode

# change working directory to current folder
os.chdir(os.path.dirname(__file__))

# connect mySQL database
try:
    con=mysql.connector.connect(user='root',password='asdfghjkl;\'',database='aus_sold_houses')
    print("Database connected sucessfully!")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit()

# select data from database
sql = """ SELECT COUNT(*)AS total_sold, AVG(sold_price) as avg_price, YEAR(sold_date) as year
    FROM aus_sold_houses.victoria
    WHERE sold_date is not null and sold_price is not null AND YEAR(sold_date) > 2007
    AND sold_price < 100000000 and sold_price > 10000
    GROUP BY YEAR(sold_date);""".format('victoria')
cursor = con.cursor(dictionary=True, buffered=True)
cursor.execute(sql)
row = cursor.fetchall()
print(row)
con.close()