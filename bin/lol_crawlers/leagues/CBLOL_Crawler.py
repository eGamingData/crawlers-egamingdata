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

sql = "truncate cblol"

mycursor.execute(sql)

mydb.commit()

##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/cblol/cblol-2020-winter-regular-season-team-statistics/'

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

images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/14/Flamengo_eSportslogo_square.png/123px-Flamengo_eSportslogo_square.png?version=bd4d9135823682896aeb663d7509415d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e4/FURIA_Esportslogo_square.png/123px-FURIA_Esportslogo_square.png?version=3518a96b5af9944db73b66d5e4f8cf9c">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/97/INTZlogo_square.png/123px-INTZlogo_square.png?version=339c5e9bbacbe51affb34ec47b96b8af">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0d/KaBuM%21_e-Sportslogo_square.png/123px-KaBuM%21_e-Sportslogo_square.png?version=58dc740a38f59be6cce5fa74eb5af179">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/7c/PaiN_Gaminglogo_square.png/123px-PaiN_Gaminglogo_square.png?version=db6a37a1dd2dc93285a31907a234a775">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/2/24/Prodigy_Esportslogo_square.png/123px-Prodigy_Esportslogo_square.png?version=43d528fe0d258f56f8b4d19237180a2f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/1c/Santos_e-Sportslogo_square.png/123px-Santos_e-Sportslogo_square.png?version=01f50578710bc7a172f7c890a58f131d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/34/Vivo_Keydlogo_square.png/123px-Vivo_Keydlogo_square.png?version=ca0a13550b7b758ff1e448b2628d3a0a">']


i = 0
for line in dflist:
	sql = "INSERT INTO cblol (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate, images[i])
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1
	
############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\CBLOL\\"
filename = "CBLOL-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")
df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
