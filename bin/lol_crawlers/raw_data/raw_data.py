import sys
sys.path.append('\bin\common')
import db_config as db
from leagueoflegends import leagueoflegends_utils as utils

import mysql.connector

url='https://oracleselixir-downloadable-match-data.s3-us-west-2.amazonaws.com/2020_LoL_esports_match_data_from_OraclesElixir_20200810.csv'
utils.download_rawdata_csv(url)


#######################################################reading data from csv##########################################################

import csv

with open('input.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)



# print(data[0])



#######################################################reading data from csv###########################################################

fstr=""

for col  in data[0]:
	fstr=fstr+col.replace(" ","_")+" varchar(20) "+",\n "



# print(fstr[:-2])


createquery=f"create table if not EXISTS raw_data ({fstr[:-3]} )"



print(createquery)

db.mycursor.execute(createquery)

db.mydb.commit()


sql = "truncate raw_data"


db.mycursor.execute(sql)



db.mydb.commit()






for i in range(1,len(data)):


	str2=""

	for val in data[i]:
		str2=str2+"'"+val+"'"+","

	datas=f"INSERT INTO raw_data VALUES ({str2[:-1]})"
	# print(datas)
	mycursor.execute(datas)
	mydb.commit()

	print("exception handeled")



	


















# print(data)
