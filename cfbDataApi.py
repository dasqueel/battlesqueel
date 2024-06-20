from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import os

cfbDataKey = os.getenv('cfbDataKey')

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = cfbDataKey
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = cfbd.BettingApi(cfbd.ApiClient(configuration))
game_id = 56 # int | Game id filter (optional)
year = 2024 # int | Year/season filter for games (optional)
week = 1 # int | Week filter (optional)
season_type = 'regular' # str | Season type filter (regular or postseason) (optional) (default to regular)
team = 'team_example' # str | Team (optional)
home = 'home_example' # str | Home team filter (optional)
away = 'away_example' # str | Away team filter (optional)
conference = 'sec' # str | Conference abbreviation filter (optional)

try:
    # Betting lines
    # api_response = api_instance.get_lines(game_id=game_id, year=year, week=week, season_type=season_type, team=team, home=home, away=away, conference=conference)
    api_response = api_instance.get_lines(year=year, week=week, conference=conference)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BettingApi->get_lines: %s\n" % e)
