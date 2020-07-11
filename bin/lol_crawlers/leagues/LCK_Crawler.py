from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
from pandas import ExcelWriter
import time


import mysql.connector

##################################################### DATABASE CONNECTION ########################################################################################################################
mydb = mysql.connector.connect(
  host="146.148.2.232",
  user="root",
  passwd="Qwertyuiop7*",
  database="egamingdata"
)

mycursor = mydb.cursor()

sql = "truncate lck"

mycursor.execute(sql)

mydb.commit()
##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/lck/lck-2020-summer-regular-season-team-statistics/'

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

i = 0
############# INSERTING VALUES ############################################
for line in dflist:
	sql = "INSERT INTO lck (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated, Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate, images[i]) 
	mycursor.execute(sql, val)
	mydb.commit()
	i += 1
print("##### Inserted data into database ##### ")

############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\LCK\\"
filename = "LCK-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")
df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
