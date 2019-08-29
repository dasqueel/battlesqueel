import flask
from flask import *
from pymongo import MongoClient
from helpers.depthChart import *
from helpers.twotter import *
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#connect to mongo
mongoUrl = os.getenv('MONGO_URL')
mongoClient = MongoClient(mongoUrl)
bsDb = mongoClient.battlesqueel

# for team in bsDb.teams.find(): print team

app = flask.Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/<gameId>')
def game(gameId):
	homeTeam = {}
	awayTeam = {}
	#get each teams data
	awayTeam['abbr'] = gameId.split('@')[0]
	homeTeam['abbr'] = gameId.split('@')[1]
	awayDoc = bsDb['teams'].find_one({'abbr':awayTeam['abbr']})
	homeDoc = bsDb['teams'].find_one({'abbr':homeTeam['abbr']})

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

	#get teams tweets
	awayTeamTwitterList = awayDoc['beat']
	homeTeamTwitterList = homeDoc['beat']
	awayTeam['tweets'] = getTeamTweets(awayTeamTwitterList)
	homeTeam['tweets'] = getTeamTweets(homeTeamTwitterList)
	return render_template('game.html', homeTeam=homeTeam,awayTeam=awayTeam)

@app.route('/radio/<string:abbr>')
def radio(abbr):
	team = bsDb['teams'].find_one({'abbr': abbr})
	return jsonify({'radio' : team['radio']})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)