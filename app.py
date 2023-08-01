from flask import Markup, render_template, jsonify, Flask, request, send_file
from pymongo import MongoClient
from helpers.depthChart import *
from helpers.tweeter import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path
# import Path
import certifi
ca = certifi.where()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# connect to mongo
mongoUrl = os.getenv('battlesqueelMongoUrl')
mongoClient = MongoClient(mongoUrl, tlsCAFile=ca)

bsDb = mongoClient.bettor

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<gameId>')
def game(gameId):
    homeTeam = {}
    awayTeam = {}
    # get each teams data
    awayTeam['abbr'] = gameId.split('@')[0]
    homeTeam['abbr'] = gameId.split('@')[1]
    awayDoc = bsDb['teams'].find_one({'abbr': awayTeam['abbr']})
    homeDoc = bsDb['teams'].find_one({'abbr': homeTeam['abbr']})

    awayTeam['sbnation'] = awayDoc['sbnation']
    homeTeam['sbnation'] = homeDoc['sbnation']

    awayTeam['school'] = awayDoc['school']
    homeTeam['school'] = homeDoc['school']

    awayTeam['nickname'] = awayDoc['nickname']
    homeTeam['nickname'] = homeDoc['nickname']

    awayTeam['espnUrl'] = awayDoc['espnUrl']
    homeTeam['espnUrl'] = homeDoc['espnUrl']

    awayTeam['fourms'] = awayDoc['forums']
    homeTeam['forums'] = homeDoc['forums']

    awayTeam['statsUrl'] = awayDoc['statsUrl']
    homeTeam['statsUrl'] = homeDoc['statsUrl']

    awayTeam['notes'] = awayDoc['notes']
    homeTeam['notes'] = homeDoc['notes']

    awayTeam['depthChart'] = Markup(getNCAADepthHtml(awayDoc['depthChart']))
    homeTeam['depthChart'] = Markup(getNCAADepthHtml(homeDoc['depthChart']))

    # get teams tweets
    awayTeamTwitterList = awayDoc['beat']
    homeTeamTwitterList = homeDoc['beat']
    awayTeam['tweets'] = getTeamTweets(awayTeamTwitterList)
    homeTeam['tweets'] = getTeamTweets(homeTeamTwitterList)

    # get podcast and pdf files
    transcriptFolderPath = '/Users/squeel/transcripts/diarizedTranscripts'
    magazinesFolderPath = '/Users/squeel/magazines/phil/2023/pdfs'
    transcriptFiles = os.listdir(transcriptFolderPath)
    magazineFiles = os.listdir(magazinesFolderPath)

    awayFiles = []
    homeFiles = []

    for f in transcriptFiles:
        if awayTeam['abbr'] in f:
            newFileObj = {}
            newFileObj['path'] = f"{transcriptFolderPath}/{f}"
            newFileObj['title'] = f.split(".")[0]
            awayFiles.append(newFileObj)
        if homeTeam['abbr'] in f:
            newFileObj = {}
            newFileObj['path'] = f"{transcriptFolderPath}/{f}"
            newFileObj['title'] = f.split(".")[0]
            homeFiles.append(newFileObj)

    for f in magazineFiles:
        if awayTeam['abbr'] in f:
            newFileObj = {}
            newFileObj['path'] = f"{magazinesFolderPath}/{f}"
            newFileObj['title'] = f.split(".")[0]
            awayFiles.append(newFileObj)
        if homeTeam['abbr'] in f:
            newFileObj = {}
            newFileObj['path'] = f"{magazinesFolderPath}/{f}"
            newFileObj['title'] = f.split(".")[0]
            homeFiles.append(newFileObj)

    awayTeam["info"] = awayFiles
    homeTeam["info"] = homeFiles

    return render_template('game.html', homeTeam=homeTeam, awayTeam=awayTeam)


@app.route('/demcanes/radio/<string:abbr>')
def radio(abbr):
    team = bsDb['teams'].find_one({'abbr': abbr})
    return jsonify({'radio': team['radio']})


@app.route('/notes', methods=["DELETE"])
def note():
    team = request.args.get("team")
    note = request.args.get("note")

    result = bsDb["teams"].update_one(
        {"abbr": team},
        {"$pull": {"notes": note}}
    )

    if result.modified_count > 0:
        return("success")
    else:
        return("nope")


@app.route('/beatWriters', methods=["DELETE"])
def beatwriter():
    team = request.args.get("team")
    beatWriter = request.args.get("beatWriter")

    print(team, beatWriter)

    result = bsDb["teams"].update_one(
        {"abbr": team},
        {"$pull": {"beat": beatWriter}}
    )

    if result.modified_count > 0:
        return("success")
    else:
        return("nope")


@app.route('/get-file', methods=["GET"])
def get_file():
    filePath = request.args.get('path')
    return send_file(f"{filePath}")


if __name__ == '__main__':
    app.run()
