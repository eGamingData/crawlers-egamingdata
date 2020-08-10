import sys
sys.path.append('\bin\common')
import db_config as db
import configparser

def test_db_connection():    
    try:
        db.mycursor.execute("SELECT VERSION()")
        results = db.mycursor.fetchone()
        ver = results[0]
        if (ver is None):
            print("ERROR IN CONNECTION")
        else:
            print("SUCCESS")               
    except:
        print ("ERROR IN CONNECTION")



