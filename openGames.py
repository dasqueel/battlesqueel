import requests
from bs4 import BeautifulSoup
import subprocess
import time
import os
from pymongo import MongoClient

mongoUrl = os.getenv('battlesqueelMongoUrl')
ngrokDomain = os.getenv('ngrokDomain')
mongoClient = MongoClient(mongoUrl)
bsDb = mongoClient.bettor
teamsCol = bsDb['teams']

def open_urls_in_browser_with_max_tabs(url_list, max_tabs=15, browser_path=""):
    for i in range(0, len(url_list), max_tabs):
        chunk = url_list[i:i + max_tabs]

        if chunk:
            subprocess.Popen([browser_path, '-new-window', chunk[0]])
            time.sleep(2)

        for url in chunk[1:]:
            subprocess.Popen([browser_path, '--new-tab', url])
            time.sleep(1)

        time.sleep(4)

# firefox_nightly_path = "/Applications/Firefox Nightly.app/Contents/MacOS/firefox"
firefox_nightly_path = '/mnt/c/Program Files/Firefox Nightly/firefox.exe'

def getWeekGames(weekNum):
    url = f'https://www.cbssports.com/college-football/schedule/FBS/2024/regular/{weekNum}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    games = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tr_elements = soup.find_all('tr')

        for tr in tr_elements:
            team_names = tr.find_all('span', class_='TeamName')
            if team_names:
                awayTeam = team_names[0].get_text(strip=True)
                homeTeam = team_names[1].get_text(strip=True)
                # print(awayTeam, homeTeam)
                games.append([awayTeam, homeTeam])

    return games

def find_school_by_name(school_list, name):
    return next((school for school in school_list if school["schoolName"] == name), None)

def getWeekGamesUrls(gamesList):
    school_names = [
        {"schoolName": "Texas St.", "otherName": "Texas State"},
        {"schoolName": "BYU", "otherName": "byu"},
        {"schoolName": "So. Miss", "otherName": "Southern Miss"},
        {"schoolName": "Fresno St.", "otherName": "Fresno State"},
        {"schoolName": "Middle Tenn.", "otherName": "Middle Tennessee State"},
        {"schoolName": "W. Kentucky", "otherName": "Western Kentucky"},
        {"schoolName": "Arkansas St.", "otherName": "Arkansas State"},
        {"schoolName": "Sam Houston", "otherName": "Sam Houston State"},
        {"schoolName": "Ole Miss", "otherName": "ole miss"},
        {"schoolName": "Miss. State", "otherName": "Mississippi State"},
        {"schoolName": "Ga. Southern", "otherName": "Georgia Southern"},
        {"schoolName": "Georgia St.", "otherName": "Georgia State"},
        {"schoolName": "Boise St.", "otherName": "Boise State"},
        {"schoolName": "Colorado St.", "otherName": "Colorado State"},
        {"schoolName": "E. Michigan", "otherName": "Eastern Michigan"},
        {"schoolName": "UMass", "otherName": "Massachusetts"},
        {"schoolName": "App. St.", "otherName": "Appalachian State"},
        {"schoolName": "Kennesaw St.", "otherName": "Kennesaw State"},
        {"schoolName": "Miami (Fla.)", "otherName": "Miami (FL)"},
        {"schoolName": "Miami-OH", "otherName": "Miami (OH)"},
        {"schoolName": "Iowa St.", "otherName": "Iowa State"},
        {"schoolName": "UTEP", "otherName": "utep"},
        {"schoolName": "N. Illinois", "otherName": "Northern Illinois"},
        {"schoolName": "San Diego St.", "otherName": "San Diego State"},
        {"schoolName": "Washington St.", "otherName": "Washington State"},
        {"schoolName": "Utah St.", "otherName": "Utah State"},
        {"schoolName": "UConn", "otherName": "Connecticut"},
        {"schoolName": "Kent St.", "otherName": "Kent State"},
        {"schoolName": "SMU", "otherName": "smu"},
        {"schoolName": "San Jose St.", "otherName": "San Jose State"},
        {"schoolName": "C. Michigan", "otherName": "Central Michigan"},
        {"schoolName": "UL-Monroe", "otherName": "Louisiana-Monroe"},
        {"schoolName": "UCF", "otherName": "ucf"},
        {"schoolName": "NC State", "otherName": "North Carolina State"},
        {"schoolName": "C. Carolina", "otherName": "Coastal Carolina"},
        {"schoolName": "Jacksonville St.", "otherName": "Jacksonville State"},
        {"schoolName": "FAU", "otherName": "Florida Atlantic"},
        {"schoolName": "Michigan St.", "otherName": "Michigan State"},
        {"schoolName": "W. Michigan", "otherName": "Western Michigan"},
        {"schoolName": "TCU", "otherName": "tcu"}
    ]

    gameUrls = []

    for game in gamesList:
        awayTeamAbbr = None 
        homeTeamAbbr = None 
        awayTeam = game[0]
        homeTeam = game[1]

        awayTeamDoc = teamsCol.find_one({"school":awayTeam})
        homeTeamDoc = teamsCol.find_one({"school":homeTeam})
        if not awayTeamDoc:
            myAwayNameDict = find_school_by_name(school_names, awayTeam)
            if myAwayNameDict:
                myAwayName = myAwayNameDict['otherName']
                awayTeamDoc = teamsCol.find_one({"school":myAwayName})
                if awayTeamDoc:
                    awayTeamAbbr = awayTeamDoc['abbr']
        else:
            awayTeamAbbr = awayTeamDoc['abbr']
        if not homeTeamDoc: 
            myHomeNameDict = find_school_by_name(school_names, homeTeam)
            if myHomeNameDict:
                myHomeName = myHomeNameDict['otherName']
                homeTeamDoc = teamsCol.find_one({"school":myHomeName})
                if homeTeamDoc:
                    homeTeamAbbr = homeTeamDoc['abbr']
        else:
            homeTeamAbbr = homeTeamDoc['abbr']

        if awayTeamAbbr and homeTeamAbbr:
            gameUrl = f"{ngrokDomain}/game/{awayTeamAbbr}@{homeTeamAbbr}"
            gameUrls.append(gameUrl)

    return gameUrls

if __name__ == "__main__":
    gamesList = getWeekGames(2)
    gameUrls = getWeekGamesUrls(gamesList)
    print(len(gameUrls))
    # open_urls_in_browser_with_max_tabs(gameUrls, max_tabs=40, browser_path=firefox_nightly_path)