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

sql = "truncate ck"

mycursor.execute(sql)

mydb.commit()

##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/lck/ck-2020-summer-regular-season-team-statistics/'

user_agent = 'Chrome/80.0.3987.132 Mozilla/5.0'
r = requests.get(url, headers={'User-Agent': user_agent})
soup = BeautifulSoup(r.text, 'html.parser')

print("##### Retrieving data... #####")

tables = soup.find_all('table')

date=soup.find("em")
lastupdateddate=date.get_text().replace("For a full list of abbreviations and explanations, check the Definitions page.","").replace("Last Updated:","").strip()

df = pd.read_html(str(tables))[0]

dflist=df.values.tolist()

print("##### Data retrieved successfully #####")

print(dflist[0])

images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e0/Awesome_Spearlogo_square.png/123px-Awesome_Spearlogo_square.png?version=69824e1f9ecbfd2a103805dc2a15f7b2">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/4f/Element_Mysticlogo_square.png/123px-Element_Mysticlogo_square.png?version=6fb45e581ddfaec688d0c776c46c1c8f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/36/ESports_Connectedlogo_square.png/123px-ESports_Connectedlogo_square.png?version=0ed21abf85bf806ace9f7500d4a040f5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/6/6a/Griffinlogo_square.png/123px-Griffinlogo_square.png?version=5e954676335234b9f3e44c12b0185a5c">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0f/HyFresh_Bladelogo_square.png/123px-HyFresh_Bladelogo_square.png?version=a89ea257c195d56656d463ea51a48fc9">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/3a/Jin_Air_Green_Wingslogo_square.png/123px-Jin_Air_Green_Wingslogo_square.png?version=7eec86e13ff793b719212f91398f1f4d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/44/OZ_Gaminglogo_square.png/123px-OZ_Gaminglogo_square.png?version=7bb82a424cdb5fffd5aa2a70950ee953">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/7c/RunAwaylogo_square.png/123px-RunAwaylogo_square.png?version=f222197839e03be00dd93b13cf2ef9a2">']


i = 0
for line in dflist:
	sql = "INSERT INTO ck (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate, images[i])
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1

print("##### Inserted data into database ##### ")

############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\CK\\"
filename = "CK-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")
df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
