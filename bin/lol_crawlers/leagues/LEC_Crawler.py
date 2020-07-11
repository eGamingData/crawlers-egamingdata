from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
from pandas import ExcelWriter
import time
import leaguepedia_parser

import mysql.connector

##################################################################################################################################################################################
mydb = mysql.connector.connect(
  host="146.148.2.232",
  user="root",
  passwd="Qwertyuiop7*",
  database="egamingdata"
)

mycursor = mydb.cursor()

sql = "truncate lec"

mycursor.execute(sql)

mydb.commit()

##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/eu/lec-2020-summer-regular-season-team-statistics/'

user_agent = 'Chrome/80.0.3987.132 Mozilla/5.0'
r = requests.get(url, headers={'User-Agent': user_agent})
soup = BeautifulSoup(r.text, 'html.parser')

print("##### Retrieving data... #####")

date=soup.find("em")
lastupdateddate=date.get_text().replace("For a full list of abbreviations and explanations, check the Definitions page.","").replace("Last Updated:","").strip()

tables = soup.find_all('table')

df = pd.read_html(str(tables))[0]

df.fillna(0, inplace=True)

dflist=df.values.tolist()

print("##### Data retrieved successfully #####")

print(dflist[0])

############### INSERTING TEAM IMAGES #################################
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/91/Excel_Esportslogo_square.png/123px-Excel_Esportslogo_square.png?version=d36c97a673a11c47923de5850375c7a5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0f/FC_Schalke_04_Esportslogo_square.png/123px-FC_Schalke_04_Esportslogo_square.png?version=0f217a167e05ce9a52f047294ed026f5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/fc/Fnaticlogo_square.png/123px-Fnaticlogo_square.png?version=0c79180962b7260f04ee01104086e6a8">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/77/G2_Esportslogo_square.png/123px-G2_Esportslogo_square.png?version=46f8bd541c056356584b6209379cf7a9">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/3c/MAD_Lionslogo_square.png/123px-MAD_Lionslogo_square.png?version=690efa5db34af59d2ae0fc59900dc959">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/9a/Misfits_Gaminglogo_square.png/123px-Misfits_Gaminglogo_square.png?version=be4f32c356da77c32a457241fbef8ef8">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/12/Origenlogo_square.png/123px-Origenlogo_square.png?version=84338bcc101e315c2c75696250babb7e">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/a4/Rogue_%28European_Team%29logo_square.png/123px-Rogue_%28European_Team%29logo_square.png?version=f8c7a01963654a0edc32db8ac6c50003">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/4f/SK_Gaminglogo_square.png/123px-SK_Gaminglogo_square.png?version=ac867fe6ccb226a337fd0005928ba99f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/8/86/Team_Vitalitylogo_square.png/123px-Team_Vitalitylogo_square.png?version=64ccfea7cf7b23f9261ecf0778bcfed2">']

i = 0
############# INSERTING VALUES ############################################
for line in dflist:
	sql = "INSERT INTO lec (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate, images[i]) 
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1

print("##### Inserted data into database ##### ")

############# FILE CREATION ############################################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\LEC\\"
filename = "LEC-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")

df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
