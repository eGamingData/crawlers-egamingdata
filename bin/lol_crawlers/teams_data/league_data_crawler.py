#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils
import db_config as db

TABLE = "lol_teams_data"

#Clear database table for new insert
utils.clear_db_table(TABLE)
print("Table " + TABLE + " cleared...")

db.mycursor.execute("SELECT league, league_name, teams_data_point FROM lol_leagues")
leagues = db.mycursor.fetchall()
print("Selected leagues...")

for league in leagues:
    
    data_point = league[2]
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

    #Getting team images
    teams = utils.get_league_teams(league[0])
    images_list = utils.get_team_image(teams)
    
    #Database Insert
    utils.save_team_data(teams_list, soup, league_acronym, TABLE, images_list)
    print("Data for " + league_acronym + " inserted..." )
    driver.quit()

print('Teams data successfully inserted')