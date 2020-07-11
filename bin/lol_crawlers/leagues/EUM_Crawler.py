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

sql = "truncate eum"

mycursor.execute(sql)

mydb.commit()
##################################################################################################################################################################################################

url = 'https://oracleselixir.com/statistics/eu/eu-masters-spring-2020-team-statistics/'

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

for line in dflist:
	sql = "INSERT INTO eum (Team, Gp,W,L,agt,k,D,KD,CKPM,GPR,GSPD,EGR,MLR,GD15,FB,FT,F3T,HLD,FD,DRG,ELD,FBN,BN,LNE,JNG,WPM,CWPM,WCPM,Last_Updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],lastupdateddate)
	mycursor.execute(sql, val)
	mydb.commit()

print("##### Inserted data into database ##### ")

############# FILE CREATION ###########################
date = time.strftime("%d-%m-%Y")
path = "C:\\Users\Administrator\\Desktop\\Crawlers\\LeagueOfLegends\\EUMasters\\"
filename = "EUM-" + date + ".xlsx"
pathfile = path + filename

print(df)

print("##### Creating backup data file ##### ")
df.to_excel(pathfile)

print("##### Backup data file saved in " + pathfile +  " ##### ")
