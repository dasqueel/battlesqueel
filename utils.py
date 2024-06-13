from pymongo import MongoClient
import os

mongoUrl = os.getenv('battlesqueelMongoUrl')
mongoClient = MongoClient(mongoUrl)
bsDb = mongoClient.bettor
teamsCol = bsDb['teams']

def createTeamAggNotesFile():
    teamDocs = teamsCol.find()
    
    for teamDoc in teamDocs:
        abbr = teamDoc["abbr"]
        abbr = abbr.replace(" ", "-")
        # print(abbr)

        with open(f"aggNotes/{abbr}.txt", 'w') as file:
            file.write("")

    # print(teamsCol.count_documents({}))

import os

transPath = os.getenv('transPath')

def getTeamTrans(teamAbbr):
    matching_files = []

    for root, dirs, files in os.walk(transPath):
        for filename in files:
            if filename.endswith('.txt') and f"-{teamAbbr}" in filename:
                fileDoc = {
                    'path': os.path.join(root, filename).replace("/home/squeel/dev/summy/diarizedTranscripts/",""),
                    'fileName': filename
                }
                matching_files.append(fileDoc)

    return matching_files

if __name__ == "__main__":
    matching_files = getTeamTrans("-tol")
    print(matching_files)