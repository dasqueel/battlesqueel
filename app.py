from flask import Markup, render_template, jsonify, Flask
from pymongo import MongoClient
from helpers.depthChart import *
from helpers.twotter import *
import os
from os.path import join, dirname
from dotenv import load_dotenv
import certifi
ca = certifi.where()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# connect to mongo
mongoUrl = os.getenv('MONGO_URL')
mongoClient = MongoClient(mongoUrl)
# mongoClient = MongoClient('mongodb+srv://squeel:sports1578@cluster0.i6ili.mongodb.net/', tlsCAFile=ca)
bsDb = mongoClient.bettor

# for team in bsDb.teams.find(): print team

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

    awayTeam['depthChart'] = Markup(getNCAADepthHtml(awayDoc['depthChart']))
    homeTeam['depthChart'] = Markup(getNCAADepthHtml(homeDoc['depthChart']))

    # get teams tweets
    awayTeamTwitterList = awayDoc['beat']
    homeTeamTwitterList = homeDoc['beat']
    awayTeam['tweets'] = getTeamTweets(awayTeamTwitterList)
    homeTeam['tweets'] = getTeamTweets(homeTeamTwitterList)
    return render_template('game.html', homeTeam=homeTeam, awayTeam=awayTeam)


@app.route('/demcanes/radio/<string:abbr>')
def radio(abbr):
    team = bsDb['teams'].find_one({'abbr': abbr})
    return jsonify({'radio': team['radio']})


# put the gui stuff in?
if __name__ == '__main__':
    app.run()
