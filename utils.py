from pymongo import MongoClient, errors
import os
import re
import spacy
import json
import pprint
from bs4 import BeautifulSoup
import requests
from rapidfuzz import fuzz
import time

mongoUrl = os.getenv('battlesqueelMongoUrl')
ngrokDomain = os.getenv('ngrokDomain')
mongoClient = MongoClient(mongoUrl)
bsDb = mongoClient.bettor
teamsCol = bsDb['teams']
cfbPlayersCol = bsDb['cfbPlayers']

cfbPlayersCol.create_index("id", unique=True)

def createTeamAggNotesFile():
    teamDocs = teamsCol.find()
    
    for teamDoc in teamDocs:
        abbr = teamDoc["abbr"]
        abbr = abbr.replace(" ", "-")
        # print(abbr)

        with open(f"aggNotes/{abbr}.txt", 'w') as file:
            file.write("")

    # print(teamsCol.count_documents({}))

transPath = os.getenv('transPath')
sumsPath = os.getenv('sumsPath')
steelePath = os.getenv('steelePath')

def isTeamAbbrInFilename(filename, teamAbbr):
    pattern = r'[-.]'
    hyphenSplits = re.split(pattern, filename)
    result = False
    for hyphenSplit in hyphenSplits:
        if teamAbbr == hyphenSplit:
            result = True
            break

    return result

def getTeamTrans(teamAbbr):
    matching_files = []

    for root, dirs, files in os.walk(transPath):
        for filename in files:
            # if filename.endswith('.txt') and f"-{teamAbbr}" in filename:
            if filename.endswith('.txt') and isTeamAbbrInFilename(filename, teamAbbr):
                fileDoc = {
                    'path': os.path.join(root, filename).replace("/home/squeel/dev/summy/diarizedTranscripts/",""),
                    'fileName': filename
                }
                matching_files.append(fileDoc)

    return matching_files

def getTeamSums(teamAbbr):
    matching_files = []

    for root, dirs, files in os.walk(sumsPath):
        for filename in files:
            if filename.endswith('.txt') and isTeamAbbrInFilename(filename, teamAbbr):
                fileDoc = {
                    'path': os.path.join(root, filename).replace("/home/squeel/dev/summy/summaries/",""),
                    'fileName': filename
                }
                matching_files.append(fileDoc)

    return matching_files

def getSteele(teamAbbr):
    return f"{ngrokDomain}/steele/{teamAbbr}.pdf"

def extract_names_from_file(file_path):
    # nlp = spacy.load("en_core_web_trf")
    nlp = spacy.load("en_core_web_lg")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    doc = nlp(content)

    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    return names

def insertPlayersMongo(position):
    with open(f'./json/{position}.json', 'r') as file:
        players = json.load(file)

    keysRemove = ["college", "age", "current_eligible_year", "meets_snap_minimum", "team_slug", "jersey_number"]

    for player in players:
        player["position"] = player["position"].lower()
        player["grade_position"] = player["grade_position"].lower()
        player["team_name"] = player["team_name"].lower()
        player["name"] = player["name"].lower()
        for key in keysRemove:
            if key in player:
                del player[key]

    # cfbPlayersCol.insert_many(players)

def extract_full_name(player):
    suffix_pattern = re.compile(r'\s+(RS\s+)?(SR|JR|SO|FR|GR)(/TR)?$', re.IGNORECASE)
    player = suffix_pattern.sub('', player)
    if ', ' in player:
        last_name, first_name = player.split(', ')
        return f"{first_name} {last_name}"
    else:
        return player

def getOurlandsPlayersObjsDirtyClean(teamDepthUrl):
    r = requests.get(teamDepthUrl)
    soup = BeautifulSoup(r.text, 'html.parser')

    td_tags = soup.find_all('td')
    playerTdEls = [td for td in td_tags if td.find('a') and ',' in td.find('a').text]

    cleanDirtyOurLadObjs = []

    for td in playerTdEls:
        dirtyPlayerTxt = td.get_text()
        try:
            cleanName = extract_full_name(dirtyPlayerTxt)
            cleanDirtyObj = {}
            cleanDirtyObj['clean'] = cleanName
            cleanDirtyObj['dirty'] = dirtyPlayerTxt
            if cleanDirtyObj not in cleanDirtyOurLadObjs:
                cleanDirtyOurLadObjs.append(cleanDirtyObj)
        except:
            print(f"error: {dirtyPlayerTxt}")
            # if dirtyPlayerTxt not in ourlandPlayers:
            #     ourlandPlayers.append(dirtyPlayerTxt)

    return(cleanDirtyOurLadObjs)

def getPffPlayerObj(olDirtyName, teamAbbr, pffTeamName):
    teamDoc = teamsCol.find_one({"abbr":teamAbbr})
    olPffNamesDict = teamDoc['olPffNameDict']
    # pffPlayerNameObj = next((d for d in playerNamesTranslationsObjs if d.get("olDirty") == olDirtyName), None)
    pffPlayerNameObj = olPffNamesDict[olDirtyName]
    pffPlayerObj = cfbPlayersCol.find_one({"team_name": pffTeamName, "name": pffPlayerNameObj['pff']})

    playerPos = pffPlayerObj['position']

    if playerPos == 'qb':
        pffPlayerObj['gradesToShow'] = {
            'O' : pffPlayerObj['offense'],
            'P' : pffPlayerObj['pass'],
            # 'pass_snaps' : pffPlayerObj['pass_snaps'],
            'R' : pffPlayerObj['run'],
            # 'run_snaps' : pffPlayerObj['run_snaps'],
        }
    elif playerPos == 'hb':
        pffPlayerObj['gradesToShow'] = {
            'O' : pffPlayerObj['offense'],
            # 'overall_snaps' : pffPlayerObj['overall_snaps'],
            'Run' : pffPlayerObj['run'],
            # 'run_snaps' : pffPlayerObj['run_snaps'],
            'Rec' : pffPlayerObj['receiving'],
            # 'receiving_snaps' : pffPlayerObj['receiving_snaps'],
            'PB' : pffPlayerObj['pass_block'],
            # 'pass_block_snaps' : pffPlayerObj['pass_block_snaps'],
        }
    elif playerPos == 'wr':
        pffPlayerObj['gradesToShow'] = {
            'O' : pffPlayerObj['offense'],
            # 'overall_snaps' : pffPlayerObj['overall_snaps'],
            'Rec' : pffPlayerObj['receiving'],
            # 'receiving_snaps' : pffPlayerObj['receiving_snaps'],
            'RB' : pffPlayerObj['run_block'],
            # 'run_block_snaps' : pffPlayerObj['run_block_snaps'],
        }
    elif playerPos == 'te':
        pffPlayerObj['gradesToShow'] = {
            'O' : pffPlayerObj['offense'],
            # 'overall_snaps' : pffPlayerObj['overall_snaps'],
            'Rec' : pffPlayerObj['receiving'],
            # 'receiving_snaps' : pffPlayerObj['receiving_snaps'],
            'RB' : pffPlayerObj['run_block'],
            # 'run_block_snaps' : pffPlayerObj['run_block_snaps'],
        }
    elif playerPos == 't' or playerPos == 'g' or playerPos == 'c':
        pffPlayerObj['gradesToShow'] = {
            'O' : pffPlayerObj['offense'],
            # 'overall_snaps' : pffPlayerObj['overall_snaps'],
            # 'Rank' : pffPlayerObj['offense_ranked'],
            'PB' : pffPlayerObj['pass_block'],
            # 'pass_block_snaps' : pffPlayerObj['pass_block_snaps'],
            'RB' : pffPlayerObj['run_block'],
            # 'run_block_snaps' : pffPlayerObj['run_block_snaps'],
        }
    elif playerPos == 'di' or playerPos == 'ed':
        pffPlayerObj['gradesToShow'] = {
            'D' : pffPlayerObj['defense'],
            # 'defense_snaps' : pffPlayerObj['defense_snaps'],
            # 'Rank' : pffPlayerObj['defense_ranked'],
            'RD' : pffPlayerObj['run_defense'],
            # 'run_defense_snaps' : pffPlayerObj['run_defense_snaps'],
            'PR' : pffPlayerObj['pass_rush'],
            # 'pass_rush_snaps' : pffPlayerObj['pass_rush_snaps'],
        }
    elif playerPos == 'lb':
        pffPlayerObj['gradesToShow'] = {
            'D' : pffPlayerObj['defense'],
            # 'defense_snaps' : pffPlayerObj['defense_snaps'],
            # 'Rank' : pffPlayerObj['defense_ranked'],
            'RD' : pffPlayerObj['run_defense'],
            # 'run_defense_snaps' : pffPlayerObj['run_defense_snaps'],
            'PR' : pffPlayerObj['pass_rush'],
            # 'pass_rush_snaps' : pffPlayerObj['pass_rush_snaps'],
            'C' : pffPlayerObj['coverage'],
            # 'coverage_snaps' : pffPlayerObj['coverage_snaps'],
        }
    elif playerPos == 'cb' or playerPos == 's':
        pffPlayerObj['gradesToShow'] = {
            'D' : pffPlayerObj['defense'],
            # 'defense_snaps' : pffPlayerObj['defense_snaps'],
            # 'Rank' : pffPlayerObj['defense_ranked'],
            'C' : pffPlayerObj['coverage'],
            # 'coverage_snaps' : pffPlayerObj['coverage_snaps'],
            'RD' : pffPlayerObj['run_defense'],
            # 'run_defense_snaps' : pffPlayerObj['run_defense_snaps'],
        }
    elif playerPos == 'k':
        pffPlayerObj['gradesToShow'] = {
            'K' : pffPlayerObj['fg_ep_kicker'],
            'KO' : pffPlayerObj['kickoff_kicker'],
        }
    elif playerPos == 'p':
        pffPlayerObj['gradesToShow'] = {
            'P' : pffPlayerObj['punter'],
            'Rank' : pffPlayerObj['punter_rank'],
        }
    
    return(pffPlayerObj)

def updateOlPffDocs():
    # teamDoc = teamsCol.find_one({"abbr":"mia"})
    teamDocs = teamsCol.find({"olPffNames": {"$exists": True}})
    # print(olPffObjs)
    for teamDoc in teamDocs:
        olPffObjs = teamDoc['olPffNames']
        teamAbbr = teamDoc['abbr']
        newPffObj = {}
        for olPffObj in olPffObjs:
            newPffObj[olPffObj['olDirty']] = {
                'olDirty' : olPffObj['olDirty'],
                'olClean' : olPffObj['olClean'],
                'pff' : olPffObj['pff']
            }

        # pprint.pprint(newPffObj)
        if teamsCol.update_one({"abbr":teamAbbr}, {"$set" : {"olPffNameDict": newPffObj }}):
            print(f"UPDATED : {teamAbbr}")

def joinPffOurlandsAndInsert(teamPff, teamAbbr, teamDepthUrl):
    ourlandsPlayersObjsDirtyClean = getOurlandsPlayersObjsDirtyClean(teamDepthUrl)
    pffPlayers = cfbPlayersCol.find({"team_name" :teamPff}, {"name":1, "_id":0})
    pffPlayers = [doc['name'] for doc in pffPlayers]

    playerObjs = []

    for pffPlayer in pffPlayers:
        for olPlayer in ourlandsPlayersObjsDirtyClean:
            olCleanLower = olPlayer['clean'].lower()
            olDirty = olPlayer['dirty']
            score = fuzz.ratio(pffPlayer, olCleanLower)
            if score > 85.0:
                playerObj = {}
                playerObj["olClean"] = olCleanLower
                playerObj["olDirty"] = olDirty
                playerObj["pff"] = pffPlayer
                playerObjs.append(playerObj)
    # for player in playerObjs: pprint.pprint(f"{player}")

    if teamsCol.update_one({"abbr":teamAbbr}, {"$set" : {"olPffNames": playerObjs }}):
        print(f"UPDATED : {teamAbbr}")
        time.sleep(5)

def updatePffOlPlayerNames():
    teamDocs = teamsCol.find()
    startDoing = False
    for teamDoc in teamDocs:
        try:
            pffTeamName = teamDoc['pffTeamName']
            teamAbbr = teamDoc['abbr']
            depthChartUrl = teamDoc['depthChart']

            if startDoing:
                joinPffOurlandsAndInsert(pffTeamName, teamAbbr, depthChartUrl)
        except KeyError as key_error:
            print(f"KeyError: Missing key {key_error} in document {teamDoc}")
        except errors.CursorNotFound:
            print("CursorNotFound exception caught. The cursor has timed out or is no longer available.")
        except Exception as e:
            print(f"failed {teamAbbr} due to error: {e}")

if __name__ == "__main__":
    # matching_files = getTeamSums("neb")
    # print(matching_files)
    # file_path = f'{transPath}/betusCfbPicks/betusCfbPicks-06-20-Wf5FT1OCX8c-bsu.txt'
    # names = extract_names_from_file(file_path)
    # positions = ['QB', 'S', 'T', 'TE', 'WR', 'ED', 'G', 'HB', 'LB', 'K', 'P', 'C', 'DI', 'CB']
    # insertPlayersMongo('K')
    print('hi')
    # updateOlPffDocs()
