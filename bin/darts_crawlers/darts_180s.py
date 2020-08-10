from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
from pandas import ExcelWriter
import re
from selenium import webdriver
import time
import numpy as np
import mysql.connector
import sys
sys.path.append('\bin\common')
import db_config as db


sql = "truncate darts_180s"
db.mycursor.execute(sql)
db.mydb.commit()   

ol_result = []
empty = 0
i = 1

while empty == 0:    
    url = 'https://www.dartsdatabase.co.uk/PlayerStats.aspx?statKey=23&pg=' + str(i)
    print(url)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", options=options)
    driver.get(url)
    time.sleep(5)
    squadPage=driver.page_source
    soup = BeautifulSoup(squadPage, 'html.parser')


    #Function to split a records list into X equal element matrix.
    def split_list (x, records):
       return [records[i:i+x] for i in range(0, len(records), x)]

    rows =  soup.find_all("td", style=lambda style: style and style.startswith("BORDER-RIGHT:"))
    print(rows)
    
    ul_result = []

    for row in rows:
        print(row.text)
        ul_result.append(row.text)

    i += 1


    ol_result = split_list(4, ul_result)
    del ol_result[0]

    print(ol_result[1][1])



    if  ol_result[2][2] == "\xa0":
        empty = 1
    else: 
                
        table_name = "darts_180s"

        for result in ol_result:    
            sql = "INSERT INTO darts_180s (rank, player, country, hundreds) VALUES (%s,%s,%s,%s)"
            val = (result[0],result[1],result[2],result[3]) 
            db.mycursor.execute(sql, val)
            db.mydb.commit()

        driver.quit()
