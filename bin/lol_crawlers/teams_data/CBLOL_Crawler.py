#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils

## GLOBAL VARIABLES ##
table_name = 'cblol'
url = 'https://oracleselixir.com/stats/teams/byTournament/CBLOL%2F2020%20Season%2FSplit%202'

#Clear database table for new insert
utils.clear_db_table(table_name)

options = utils.webdriver.ChromeOptions()
options.add_argument("--headless")
driver = utils.webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", options=options)
driver.get(url)
utils.time.sleep(10)
squadPage=driver.page_source
soup = utils.BeautifulSoup(squadPage, 'html.parser')

#List of data to gather from datapoint
label_list = ['Team', 'GP', 'W', 'L', 'AGT', 'K', 'D', 'KD', 'CKPM', 'GPR', 'GSPD', 'EGR', 'MLR', 'GD15', 'FB%',
              'FT%', 'F3T%', 'HLD%', 'FD%', 'DRG%', 'ELD%', 'FBN%', 'BN%', 'LNE%', 'JNG%', 'WPM', 'CWPM', 'WCPM']

result = soup.find_all("div", attrs={"label":True})
records = []
for elem in result:
    records.append(elem.text) 

#Organized data by team
teams_list = utils.split_list(28, records)

#TO-DO: Create a separate method (leagueoflegends_utils.py) to retrieve team images from database
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/14/Flamengo_eSportslogo_square.png/123px-Flamengo_eSportslogo_square.png?version=bd4d9135823682896aeb663d7509415d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e4/FURIA_Esportslogo_square.png/123px-FURIA_Esportslogo_square.png?version=3518a96b5af9944db73b66d5e4f8cf9c">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/97/INTZlogo_square.png/123px-INTZlogo_square.png?version=339c5e9bbacbe51affb34ec47b96b8af">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0d/KaBuM%21_e-Sportslogo_square.png/123px-KaBuM%21_e-Sportslogo_square.png?version=58dc740a38f59be6cce5fa74eb5af179">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/7c/PaiN_Gaminglogo_square.png/123px-PaiN_Gaminglogo_square.png?version=db6a37a1dd2dc93285a31907a234a775">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/2/24/Prodigy_Esportslogo_square.png/123px-Prodigy_Esportslogo_square.png?version=43d528fe0d258f56f8b4d19237180a2f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/1c/Santos_e-Sportslogo_square.png/123px-Santos_e-Sportslogo_square.png?version=01f50578710bc7a172f7c890a58f131d">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/34/Vivo_Keydlogo_square.png/123px-Vivo_Keydlogo_square.png?version=ca0a13550b7b758ff1e448b2628d3a0a">']

#Database Insert
utils.save_data(teams_list, table_name, soup, images)
print("Insert OK...")

driver.quit()
