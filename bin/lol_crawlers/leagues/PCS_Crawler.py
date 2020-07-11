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

sql = "truncate pcs"

mycursor.execute(sql)

mydb.commit()

##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/lms/pcs-2020-summer-regular-season-team-statistics/'

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


i = 0
for line in dflist:
	sql = "INSERT INTO pcs (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate, images[i])
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1

print("##### Inserted data into database ##### ")

############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\PCS\\"
filename = "PCS-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")

df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
