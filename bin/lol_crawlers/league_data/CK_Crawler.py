from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
from pandas import ExcelWriter
import re
from selenium import webdriver
import time
import numpy as np
import leagueoflegends_utils as utils
import mysql.connector

## GLOBAL VARIABLES ##

table_name = 'ck'
url = 'https://oracleselixir.com/stats/teams/byTournament/Challengers%20Korea%2F2020%20Season%2FSummer%20Season'

#Clear database table for new insert
utils.clear_db_table(table_name)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", options=options)
driver.get(url)
time.sleep(10)
squadPage=driver.page_source
soup = BeautifulSoup(squadPage, 'html.parser')

#List of data to gather from datapoint
label_list = ['Team', 'GP', 'W', 'L', 'AGT', 'K', 'D', 'KD', 'CKPM', 'GPR', 'GSPD', 'EGR', 'MLR', 'GD15', 'FB%',
              'FT%', 'F3T%', 'HLD%', 'FD%', 'DRG%', 'ELD%', 'FBN%', 'BN%', 'LNE%', 'JNG%', 'WPM', 'CWPM', 'WCPM']

result = soup.find_all("div", attrs={"label":True})
records = []
for elem in result:
    records.append(elem.text) 

#Organized data by team
teams_list = utils.split_list(28, records)

#TO-DO: Create a separate method (leagueoflegends_utils.py) to retrieve team images from database
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e0/Awesome_Spearlogo_square.png/123px-Awesome_Spearlogo_square.png?version=69824e1f9ecbfd2a103805dc2a15f7b2">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/4f/Element_Mysticlogo_square.png/123px-Element_Mysticlogo_square.png?version=6fb45e581ddfaec688d0c776c46c1c8f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/36/ESports_Connectedlogo_square.png/123px-ESports_Connectedlogo_square.png?version=0ed21abf85bf806ace9f7500d4a040f5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/6/6a/Griffinlogo_square.png/123px-Griffinlogo_square.png?version=5e954676335234b9f3e44c12b0185a5c">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0f/HyFresh_Bladelogo_square.png/123px-HyFresh_Bladelogo_square.png?version=a89ea257c195d56656d463ea51a48fc9">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/3a/Jin_Air_Green_Wingslogo_square.png/123px-Jin_Air_Green_Wingslogo_square.png?version=7eec86e13ff793b719212f91398f1f4d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/44/OZ_Gaminglogo_square.png/123px-OZ_Gaminglogo_square.png?version=7bb82a424cdb5fffd5aa2a70950ee953">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/7c/RunAwaylogo_square.png/123px-RunAwaylogo_square.png?version=f222197839e03be00dd93b13cf2ef9a2">']

#Database Insert
utils.save_data(teams_list, table_name, soup, images)
print("Insert OK...")

driver.quit()
