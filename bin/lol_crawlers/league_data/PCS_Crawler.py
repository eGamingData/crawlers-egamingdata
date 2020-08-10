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
#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils

## GLOBAL VARIABLES ##

table_name = 'pcs'
url = 'https://oracleselixir.com/stats/teams/byTournament/PCS%2F2020%20Season%2FSummer%20Season'

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
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/a3/Ahq_eSports_Clublogo_square.png/123px-Ahq_eSports_Clublogo_square.png?version=c83bdcf1109c2654c609cc68e2ff10fa">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/07/Alpha_Esportslogo_square.png/123px-Alpha_Esportslogo_square.png?version=a0dc5ad03d4a83f0b883bed5a98eaed9">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/a9/Berjaya_Dragonslogo_square.png/123px-Berjaya_Dragonslogo_square.png?version=4712265ba15e1c4e25bdbfeb6efcc196">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/47/Hong_Kong_Attitudelogo_square.png/123px-Hong_Kong_Attitudelogo_square.png?version=7b24dc9d970f287f705d338d58c7a3d6">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/fa/J_Teamlogo_square.png/123px-J_Teamlogo_square.png?version=17deb7c298f24c3656e32ac2b7b753e0">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/aa/Liyab_Esportslogo_square.png/123px-Liyab_Esportslogo_square.png?version=e6b71f16bfbafa4969da142be102da09">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/d/d3/Machi_Esportslogo_square.png/123px-Machi_Esportslogo_square.png?version=d407c280bd46f086194a4da2acf715c0">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/45/Nova_Esports_%28Thai_Team%29logo_square.png/123px-Nova_Esports_%28Thai_Team%29logo_square.png?version=f7545bf182a5c57c92cfecbdf0ee520f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/48/PSG_Talonlogo_square.png/123px-PSG_Talonlogo_square.png?version=a2a130f9b90605496e91d2c63e382a97">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/d/d0/Resurgencelogo_square.png/123px-Resurgencelogo_square.png?version=38b1d1abc6b6a5c2b187f1e683bd28a0">']

#Database Insert
utils.save_data(teams_list, table_name, soup, images)
print("Insert OK...")

driver.quit()
