import sys
sys.path.append('\bin\common')
import db_config as db
import mysql.connector




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

mycursor.execute(createquery)

mydb.commit()


sql = "truncate raw_data"


mycursor.execute(sql)



mydb.commit()






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
