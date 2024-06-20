from pymongo import MongoClient
import os
import re
import spacy

mongoUrl = os.getenv('battlesqueelMongoUrl')
ngrokDomain = os.getenv('ngrokDomain')
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

if __name__ == "__main__":
    # matching_files = getTeamSums("neb")
    # print(matching_files)
    file_path = f'{transPath}/betusCfbPicks/betusCfbPicks-06-20-Wf5FT1OCX8c-bsu.txt'
    names = extract_names_from_file(file_path)
    print(names)