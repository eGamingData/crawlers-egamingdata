from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
from pandas import ExcelWriter
import re

import sys
sys.path.append('\bin\common')
import db_config as db

import mysql.connector
leagues=['lec','lcs','lck','cblol','pcs','tcl','vcs']
league_url=['https://lol.gamepedia.com/LEC/2020_Season/Summer_Season','https://lol.gamepedia.com/LCS/2020_Season/Summer_Season','https://lol.gamepedia.com/LCK/2020_Season/Summer_Season','https://lol.gamepedia.com/CBLOL_2020_Split_2','https://lol.gamepedia.com/PCS_2020_Summer','https://lol.gamepedia.com/TCL_2020_Summer','https://lol.gamepedia.com/VCS_2020_Summer']
arr_week=[]
j=0
for j in range (0,len(leagues)):
        sql = "SELECT week FROM lol_events WHERE league='"+leagues[j]+"'"
        mycursor.execute(sql)
        week = mycursor.fetchall()
        week = ''.join(week[0])
        num_week=week[4:]
        num_week=int(num_week)
        num_week=(num_week+1)
        arr_week.append('week'+str(num_week))

j=0
sql="TRUNCATE lol_events"
mycursor.execute(sql)
mydb.commit()
for j in range (0,len(leagues)):
        user_agent = 'Chrome/80.0.3987.132 Mozilla/5.0'
        r = requests.get(league_url[j], headers={'User-Agent': user_agent})

        soup = BeautifulSoup(r.text, 'html.parser')

        # This will get the div
        # rows = soup.find_all('tr', {'class': re.compile('mdv-week5')})

        results = soup.find_all('tr', attrs={'class':'mdv-'+arr_week[j]})
        # print(results)
        records = []

        for result in soup.find_all('tr', attrs={'class':'mdv-'+arr_week[j]}):
                for wrapper in result.findAll('span', attrs={'class':'teamname'}):
                        print (wrapper.text)
                        records.append((wrapper.text))        

        teams_1 = []
        teams_2 = []

        for i in range(0, len(records)): 
            if i % 2: 
                teams_1.append(records[i]) 
            else : 
                teams_2.append(records[i])
                
          
        print('Teams 1:')
        print(teams_1)
        print('Teams 2:')
        print(teams_2)
        i = 0
        for (team1, team2) in zip(teams_2, teams_1):
                sql = "INSERT INTO lol_events (league, team_one, team_two, week) VALUES (%s,%s,%s,%s)"
                val = (leagues[j],team1,team2,arr_week[j])
                mycursor.execute(sql, val)
        mydb.commit()
        i += 1



        

