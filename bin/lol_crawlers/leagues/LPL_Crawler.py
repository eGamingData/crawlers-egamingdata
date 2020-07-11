from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
from pandas import ExcelWriter
import time

import mysql.connector

##################################################################################################################################################################################
mydb = mysql.connector.connect(
  host="146.148.2.232",
  user="root",
  passwd="Qwertyuiop7*",
  database="egamingdata"
)

mycursor = mydb.cursor()

sql = "truncate lpl"

mycursor.execute(sql)

mydb.commit()

##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/lpl/lpl-2020-summer-regular-season-team-statistics/'

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

images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/91/Bilibili_Gaminglogo_square.png/123px-Bilibili_Gaminglogo_square.png?version=fe84610eef61a3de21d2fec18b3e40ba">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/16/Dominus_Esportslogo_square.png/123px-Dominus_Esportslogo_square.png?version=ba0d54e0365772c503a4ea10cec5cdd8">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/5/56/EDward_Gaminglogo_square.png/123px-EDward_Gaminglogo_square.png?version=4ebdb366b8b5f572c89ac371e6dbfc94">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/2/23/EStar_%28Chinese_Team%29logo_square.png/123px-EStar_%28Chinese_Team%29logo_square.png?version=266232f90cb1c5ceb996c513bc9dab22">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/b/b1/FunPlus_Phoenixlogo_square.png/123px-FunPlus_Phoenixlogo_square.png?version=59f03e4dc123c53ea1b1dcfc0e5e51b5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e4/Invictus_Gaminglogo_square.png/123px-Invictus_Gaminglogo_square.png?version=e60d852a5148fef54c67dc2b1e4b2f6f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/00/JD_Gaminglogo_square.png/123px-JD_Gaminglogo_square.png?version=2747327310c9056d3b8ccdad6cf1e90f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/5/55/LGD_Gaminglogo_square.png/123px-LGD_Gaminglogo_square.png?version=cb5c311b6666911b876503a53224e222">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/d/d5/LNG_Esportslogo_square.png/123px-LNG_Esportslogo_square.png?version=edc71fa5a48070418bcce84239f6b214">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0d/Oh_My_Godlogo_square.png/123px-Oh_My_Godlogo_square.png?version=e47af1c91974f5edfc7c5bba6931e229">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/2/26/Rogue_Warriorslogo_square.png/123px-Rogue_Warriorslogo_square.png?version=c26311e2fc46c3e649b4c45e83507687">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/eb/Royal_Never_Give_Uplogo_square.png/123px-Royal_Never_Give_Uplogo_square.png?version=146826fc62b083972f20cc4ca603238e">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/31/Suninglogo_square.png/123px-Suninglogo_square.png?version=30b6a8597b36f4e7e7df44132de59f69">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0a/Team_WElogo_square.png/123px-Team_WElogo_square.png?version=56f767c33985f4160cf62ca79536e6b9">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/46/Top_Esportslogo_square.png/123px-Top_Esportslogo_square.png?version=96d38b4179da6fe94b7c0c98265f770e">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/ef/Vici_Gaminglogo_square.png/123px-Vici_Gaminglogo_square.png?version=29633fba79be6abcea3acce67cc00bb6">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/3d/Victory_Fivelogo_square.png/123px-Victory_Fivelogo_square.png?version=12c5726510e0951c10506ab8651b25e9">']


i = 0

for line in dflist:
	sql = "INSERT INTO lpl (Team,Gp,W,L,agt,k,D,KD,CKPM,DRG,BN,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],lastupdateddate, images[i])
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1

print("##### Inserted data into database ##### ")

############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\LPL\\"
filename = "LPL-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")
df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
