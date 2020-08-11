#Author: Xavier Garcia Clavero
#Organization: eGamingData
#Creation date Date: 12/07/2020
#Last Update: 10/08/2020
#Description: Common functions for League of Legends esports teams data scraping.

## Imports ##########################
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import pandas as pd
from pandas import ExcelWriter
import mysql.connector
import time
import requests
import requests
import xlrd
import sys
sys.path.append('\bin\common')
import db_config as db
####################################

#Function to split a records list into X equal element matrix.
def split_list (x, records):
   return [records[i:i+x] for i in range(0, len(records), x)]

#Function to get last data update
def get_last_update(soup):
   return soup.find('time', attrs={'datetime':True}).text

#Function to delete all records from a database table.
def clear_db_table(table_name):
   sql = "truncate " + table_name
   db.mycursor.execute(sql)
   db.mydb.commit()   

#Save teams data into database
def save_data(teams_list, soup, league):
    i = 0
    lastupdateddate = get_last_update(soup)
    for team in teams_list:
       sql = "INSERT INTO lol_league_data (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, League) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
       val = (team[0],team[1],team[2],team[3],team[4],team[5],team[6],team[7],team[8],team[9],team[10],team[11],team[12],team[13],team[14],team[15],team[16],team[17],team[18],team[19],team[20],team[21],team[22],team[23],team[24],team[25],team[26],team[27],lastupdateddate, league) 
       db.mycursor.execute(sql, val)
       db.mydb.commit()
       i += 1
       
#Downloads rawdata in csv format from url
def download_rawdata_csv(url):   
   response = requests.get(url)
   with open(os.path.join("C:\\Users\\Administrator\\Desktop\\Crawler_development\\bin\\lol_crawlers\\raw_data", "input.csv"), 'wb') as f:
       f.write(response.content)
   
   
