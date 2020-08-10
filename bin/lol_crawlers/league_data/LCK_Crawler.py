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

table_name = 'lck'
url = 'https://oracleselixir.com/stats/teams/byTournament/LCK%2F2020%20Season%2FSummer%20Season'

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
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/70/Afreeca_Freecslogo_square.png/123px-Afreeca_Freecslogo_square.png?version=3e7b76188026856871f1851af6e6eac1">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/6/6d/DAMWON_Gaminglogo_square.png/123px-DAMWON_Gaminglogo_square.png?version=4d7ea689932d8cd48577361b3590c587">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/d/d3/DRXlogo_square.png/123px-DRXlogo_square.png?version=bcc69bb3af951c72deeb18acf1b87f48">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e3/Gen.Glogo_square.png/123px-Gen.Glogo_square.png?version=3958dd9d38795d83f854b7286e445e3d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/a6/Hanwha_Life_Esportslogo_square.png/123px-Hanwha_Life_Esportslogo_square.png?version=952129656d8c0f16fbaaffa9f88c822a">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/f8/KT_Rolsterlogo_square.png/123px-KT_Rolsterlogo_square.png?version=8601e35042b9779b272b50463b438d2f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0c/SANDBOX_Gaminglogo_square.png/123px-SANDBOX_Gaminglogo_square.png?version=3dd9277194f7d9c1c97bbbca8468d7d5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/c/cc/SeolHaeOne_Princelogo_square.png/123px-SeolHaeOne_Princelogo_square.png?version=781cf44d0869ce0f5ff8e0a9a5884336">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/a2/T1logo_square.png/123px-T1logo_square.png?version=8b367d7d4703b0f9413bfb3d3d75c1d1">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e9/Team_Dynamicslogo_square.png/123px-Team_Dynamicslogo_square.png?version=71432d077a291b8ae4e3d7f30c1b199e">']

#Database Insert
utils.save_data(teams_list, table_name, soup, images)
print("Insert OK...")

driver.quit()
