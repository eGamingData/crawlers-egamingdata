#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils
import db_config as db

#Clear database table for new insert
utils.clear_db_table("lol_league_data")
print("Table lol_league_data cleared...")

db.mycursor.execute("SELECT league, data_point FROM lol_leagues")
leagues = db.mycursor.fetchall()
print("Selected leagues...")

for league in leagues:
    
    data_point = league[1]
    print("Data point: " + data_point)
    league_acronym = league [0]
    print("League: " + league_acronym)

    #TO-DO - Create a method for the driver init
    
    options = utils.webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = utils.webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", options=options)
    driver.get(data_point)
    utils.time.sleep(10)
    squadPage=driver.page_source
    soup = utils.BeautifulSoup(squadPage, 'html.parser')    

    result = soup.find_all("div", attrs={"label":True})
    records = []
    for elem in result:
        records.append(elem.text)

    #Organized data by team
    teams_list = utils.split_list(28, records)

    #TO-DO - Retrieve team images to insert at save_data()
    
    #Database Insert
    utils.save_data(teams_list, soup, league_acronym)
    print("Data for " + league_acronym + " inserted..." )
    driver.quit()
