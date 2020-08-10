#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils

## GLOBAL VARIABLES ##

table_name = 'lcs'
url = 'https://oracleselixir.com/stats/teams/byTournament/LCS%2F2020%20Season%2FSummer%20Season'

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
images = ['<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/b/b9/100_Thieveslogo_square.png/123px-100_Thieveslogo_square.png?version=c213f0c025c3e0131fb1d2686e755265">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/8/88/Cloud9logo_square.png/123px-Cloud9logo_square.png?version=2246afc8f2f9a1a0cd767904ef7c97ab">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/3/37/Counter_Logic_Gaminglogo_square.png/123px-Counter_Logic_Gaminglogo_square.png?version=7d3fd885069648129e83ff698924dff6">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/f3/Dignitaslogo_square.png/123px-Dignitaslogo_square.png?version=8f8a4f520c199c0214d57936142cbd08">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/99/Evil_Geniuses_2020logo_square.png/123px-Evil_Geniuses_2020logo_square.png?version=0b79e21e711ae0f2e27a12c83dcf3acf">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/e/e5/FlyQuestlogo_square.png/123px-FlyQuestlogo_square.png?version=931f506920bb8e9cbf56cb4f8aee8c2a">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/9/98/Golden_Guardianslogo_square.png/123px-Golden_Guardianslogo_square.png?version=58e8e988d4d9b770d3592c77b9523d75">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/b/b5/Immortalslogo_square.png/123px-Immortalslogo_square.png?version=e5bb1e0ed3b1b0be57096444449ece4c">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/f/f4/Team_Liquidlogo_square.png/123px-Team_Liquidlogo_square.png?version=580685858f29fb6655cff0324400cf10">',
          '<img style="width: 3rem;margin-right: 2rem;" src="https://gamepedia.cursecdn.com/lolesports_gamepedia_en/thumb/8/83/Team_SoloMidlogo_square.png/123px-Team_SoloMidlogo_square.png?version=706cd58f81e78e76b4298657bf3cae3c">']

#Database Insert
utils.save_data(teams_list, table_name, soup, images)
print("Insert OK...")

driver.quit()
