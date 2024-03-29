#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils

## GLOBAL VARIABLES ##

table_name = 'lec'
url = 'https://oracleselixir.com/stats/teams/byTournament/LEC%2F2020%20Season%2FSummer%20Season'

#Clear database table for new insert
utils.clear_db_table(table_name)

options = utils.webdriver.ChromeOptions()
options.add_argument("--headless")
driver = utils.webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", options=options)
driver.get(url)
utils.time.sleep(10)
squadPage=driver.page_source
soup = utils.BeautifulSoup(squadPage, 'html.parser')


result = soup.find_all("div", attrs={"label":True})
records = []
for elem in result:
    records.append(elem.text) 

#Organized data by team
teams_list = utils.split_list(28, records)

#TO-DO: Create a separate method (leagueoflegends_utils.py) to retrieve team images from database
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/91/Excel_Esportslogo_square.png/123px-Excel_Esportslogo_square.png?version=d36c97a673a11c47923de5850375c7a5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/0/0f/FC_Schalke_04_Esportslogo_square.png/123px-FC_Schalke_04_Esportslogo_square.png?version=0f217a167e05ce9a52f047294ed026f5">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/fc/Fnaticlogo_square.png/123px-Fnaticlogo_square.png?version=0c79180962b7260f04ee01104086e6a8">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/7/77/G2_Esportslogo_square.png/123px-G2_Esportslogo_square.png?version=46f8bd541c056356584b6209379cf7a9">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/3c/MAD_Lionslogo_square.png/123px-MAD_Lionslogo_square.png?version=690efa5db34af59d2ae0fc59900dc959">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/9a/Misfits_Gaminglogo_square.png/123px-Misfits_Gaminglogo_square.png?version=be4f32c356da77c32a457241fbef8ef8">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/1/12/Origenlogo_square.png/123px-Origenlogo_square.png?version=84338bcc101e315c2c75696250babb7e">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/a/a4/Rogue_%28European_Team%29logo_square.png/123px-Rogue_%28European_Team%29logo_square.png?version=f8c7a01963654a0edc32db8ac6c50003">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/4/4f/SK_Gaminglogo_square.png/123px-SK_Gaminglogo_square.png?version=ac867fe6ccb226a337fd0005928ba99f">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/8/86/Team_Vitalitylogo_square.png/123px-Team_Vitalitylogo_square.png?version=64ccfea7cf7b23f9261ecf0778bcfed2">']

#Database Insert
utils.save_data(teams_list, table_name, soup, images)
print("Insert OK...")

driver.quit()
