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

sql = "truncate naa"

mycursor.execute(sql)

mydb.commit()

##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/na/na-academy-2020-summer-regular-season-team-statistics/'

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

print(dflist[0])

print("##### Data retrieved successfully #####")

images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/b/b9/100_Thieveslogo_square.png/123px-100_Thieveslogo_square.png?version=c213f0c025c3e0131fb1d2686e755265">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/8/88/Cloud9logo_square.png/123px-Cloud9logo_square.png?version=2246afc8f2f9a1a0cd767904ef7c97ab">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/37/Counter_Logic_Gaminglogo_square.png/123px-Counter_Logic_Gaminglogo_square.png?version=7d3fd885069648129e83ff698924dff6">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/f3/Dignitaslogo_square.png/123px-Dignitaslogo_square.png?version=8f8a4f520c199c0214d57936142cbd08">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/99/Evil_Geniuses_2020logo_square.png/123px-Evil_Geniuses_2020logo_square.png?version=0b79e21e711ae0f2e27a12c83dcf3acf">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e5/FlyQuestlogo_square.png/123px-FlyQuestlogo_square.png?version=931f506920bb8e9cbf56cb4f8aee8c2a">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/98/Golden_Guardianslogo_square.png/123px-Golden_Guardianslogo_square.png?version=58e8e988d4d9b770d3592c77b9523d75">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/b/b5/Immortalslogo_square.png/123px-Immortalslogo_square.png?version=e5bb1e0ed3b1b0be57096444449ece4c">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/f4/Team_Liquidlogo_square.png/123px-Team_Liquidlogo_square.png?version=580685858f29fb6655cff0324400cf10">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/8/83/Team_SoloMidlogo_square.png/123px-Team_SoloMidlogo_square.png?version=706cd58f81e78e76b4298657bf3cae3c">']


i = 0
for line in dflist:
	sql = "INSERT INTO naa (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate, images[i])
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1

print("##### Inserted data into database ##### ")

############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\NAAcademy\\"
filename = "NAA-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")

df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
