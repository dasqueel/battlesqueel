from bs4 import BeautifulSoup
import requests
import sys

teamsMap = {
    "North Dakota": "ndsu",
    "Air Force": "af",
    "Akron": "akron",
    "Alabama": "ala",
    "Appalachian State": "appst",
    "Arizona": "ua",
    "Arizona State": "asu",
    "Arkansas": "ark",
    "Arkansas State": "arkst",
    "Army": "army",
    "Auburn": "aub",
    "Ball State": "ball",
    "Baylor": "bay",
    "Boise State": "bsu",
    "Boston College": "bc",
    "Bowling Green": "bg",
    "Buffalo": "buf",
    "California": "cal",
    "Central Michigan": "cmu",
    "Charlotte": "char",
    "Cincinnati": "cin",
    "Clemson": "clem",
    "Colorado": "cu",
    "Colorado State": "csu",
    "Connecticut": "uconn",
    "Duke": "duke",
    "East Carolina": "ecu",
    "Eastern Michigan": "emu",
    "FIU": "fiu",
    "Florida": "uf",
    "Florida Atlantic": "fau",
    "Florida State": "fsu",
    "Fresno State": "fres",
    "Georgia": "uga",
    "Georgia Southern": "gsu",
    "Georgia State": "gast",
    "Georgia Tech": "gt",
    "Hawai'i": "haw",
    "Houston": "hou",
    "Idaho": "ida",
    "Illinois": "ill",
    "Indiana": "iu",
    "Iowa": "iowa",
    "Iowa State": "isu",
    "Kansas": "ku",
    "Kansas State": "ksu",
    "Kent State": "kent",
    "Kentucky": "uk",
    "LSU": "lsu",
    "Louisiana Tech": "ltu",
    "Louisiana-Lafayette": "ull",
    "Louisiana-Monroe": "ulm",
    "Louisville": "ul",
    "Marshall": "marsh",
    "Maryland": "mary",
    "Massachusetts": "umass",
    "Memphis": "mem",
    "Miami": "mia",
    "Miami (OH)": "miaoh",
    "Michigan": "umich",
    "Michigan State": "msu",
    "Middle Tennessee": "mtst",
    "Minnesota": "min",
    "Mississippi State": "msst",
    "Missouri": "mizz",
    "Navy": "navy",
    "Nebraska": "neb",
    "Nevada": "nev",
    "New Mexico": "unm",
    "New Mexico State": "nmst",
    "North Carolina": "unc",
    "North Carolina State": "ncst",
    "North Texas": "unt",
    "Northern Illinois": "niu",
    "Northwestern": "nu",
    "Notre Dame": "nd",
    "Ohio": "ohio",
    "Ohio State": "ohst",
    "Oklahoma": "ou",
    "Oklahoma State": "okst",
    "Old Dominion": "odu",
    "Oregon": "ore",
    "Oregon State": "osu",
    "Penn State": "psu",
    "Pittsburgh": "pitt",
    "Purdue": "pur",
    "Rice": "rice",
    "Rutgers": "ru",
    "San Diego State": "sdsu",
    "San Jose State": "sjsu",
    "South Alabama": "salu",
    "South Carolina": "uscar",
    "South Florida": "usf",
    "Southern Miss": "usm",
    "Stanford": "stan",
    "Syracuse": "su",
    "Temple": "temp",
    "Tennessee": "ten",
    "Texas": "ut",
    "Texas A&M": "txam",
    "Texas State": "txst",
    "Texas Tech": "ttu",
    "Toledo": "tol",
    "Troy": "troy",
    "Tulane": "tu",
    "Tulsa": "tul",
    "UAB": "uab",
    "UCLA": "ucla",
    "UNLV": "unlv",
    "USC": "usc",
    "UTSA": "utsa",
    "Utah": "utah",
    "Utah State": "usu",
    "Vanderbilt": "vandy",
    "Virginia": "uv",
    "Virginia Tech": "vt",
    "Wake Forest": "wf",
    "Washington": "uw",
    "Washington State": "wsu",
    "West Virginia": "wvu",
    "Western Kentucky": "wku",
    "Western Michigan": "wmu",
    "Wisconsin": "wisc",
    "Wyoming": "wyo",
    "byu": "byu",
    "ole miss": "ole",
    "smu": "smu",
    "tcu": "tcu",
    "ucf": "ucf",
    "utep": "utep"
}

week = sys.argv[1]

espnUrl = 'https://www.espn.com/college-football/schedule/_/week/' + week

print espnUrl

req = requests.get(espnUrl)
# print req.text

soup = BeautifulSoup(req.text, 'html.parser')

# print soup
#
dayDivs = soup.findAll("table", {"class": "schedule has-team-logos align-left"})

# get all trs in each dayDiv
dayDiv = dayDivs[0]
trs = dayDiv.findAll("tr")
# first tr contains date information
# rest of the trs are game rows

for tr in trs:
  spans = tr.findAll('span')
  # print spans
  if len(spans) == 2:
    for span in spans:
      school = span.text
      if school in teamsMap.keys(): print school, teamsMap[school]



# print len(mydivs)
# for div in mydivs: print div


import webbrowser

urls = ["https://si.com", "https://espn.com", "https://fast.com"]


#open each url
# for url in urls:
#     webbrowser.get('chrome').open(url, new=2)

'''

import webbrowser
URLS = ("https://si.com", "https://espn.com", "https://fast.com")
browser= webbrowser.get('chrome')
first= True
for url in URLS:
    if first:
        browser.open_new(url)
        first = False
    else:
        browser.open_new_tab(url)


'''