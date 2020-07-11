




#######################################################reading data from csv##########################################################

import csv

with open('input.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)



# print(data[0])



#######################################################reading data from csv###########################################################

########################################################my sql connector##################################################

import mysql.connector



mydb = mysql.connector.connect(
 host="146.148.2.232",
  user="root",
  passwd="",
  database="egamingdata"
)

mycursor = mydb.cursor()



#########################################################my sql connector#######################################################


mycursor = mydb.cursor()

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
