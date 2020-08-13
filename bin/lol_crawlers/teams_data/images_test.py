#Import LeagueOfLegends Common Module
import sys
sys.path.append('\bin\common')
from leagueoflegends import leagueoflegends_utils as utils
import db_config as db
 

LEAGUE = 'lec'
teams = utils.get_league_teams('lec')
print(teams)
images_list = utils.get_team_image(teams)
print(images_list)



