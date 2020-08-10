import requests
import mysql.connector

import configparser
config = configparser.ConfigParser()
#TO-DO Change path to relative
config.read('C:\\Users\\Administrator\\Desktop\\Crawler_development\\bin\\common\\config.ini')


##################################################################################################################################################################################
mydb = mysql.connector.connect(
  host = config['mysqlDB']['host'],
  port = config['mysqlDB']['port'],
  user = config['mysqlDB']['user'],
  passwd = config['mysqlDB']['password'],
  database = config['mysqlDB']['database']
)
mycursor = mydb.cursor(buffered=True)
print("Connected to database...")
##################################################################################################################################################################################
