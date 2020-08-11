import sys
sys.path.append('\bin\common')
import db_config as db
from leagueoflegends import leagueoflegends_utils as utils

TEST_TEAMS_TABLE = "test_teams_data"
TEST_PLAYERS_TABLE = "test_players_data"
TEST_CHAMPIONS_TABLE = "test_champions_data"

#TO-DO - Create dummy data file to use on tests.

#TO-DO - Integrate logger library to catch and display logs/errors.

#Test saving teams data
def test_save_teams_data():
    try:
        if utils.save_team_data(test_team_list, soup, league, TEST_TEAMS_TABLE):
            print("Teams saved successfully...")
        else:
            print("Error inserting teams...")
    except:
        print("Error exectuing test...")

#Test saving players data     
def test_save_players_data():
    try:
        if save_player_data(test_players_list, soup, league, TEST_PLAYERS_TABLE):
            print("Players saved successfully...")
        else:
            print("Error inserting players...")
    except:
        print("Error exectuing test...")
        
#Test saving champions data  
def test_save_champions_data():
    try:
        if save_champions_data(test_champions_list, soup, league, TEST_CHAMPIONS_TABLE):
            print("Champions saved successfully...")
        else:
            print("Error inserting champions...")
    except:
         print("Error exectuing test...")
