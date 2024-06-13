from flask import Markup, render_template, jsonify, Flask, request, send_file, send_from_directory, render_template_string, abort
from pymongo import MongoClient
from helpers.depthChart import *
# from helpers.tweeter import *
import os
# from os.path import join, dirname
# from dotenv import load_dotenv
from pathlib import Path
# import Path
import certifi
from utils import getTeamTrans
ca = certifi.where()

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# connect to mongo
mongoUrl = os.getenv('battlesqueelMongoUrl')
transPath = os.getenv('transPath')
ngrokDomain = os.getenv('ngrokDomain')
mongoClient = MongoClient(mongoUrl, tlsCAFile=ca)

bsDb = mongoClient.bettor
podTransCol = bsDb['podTrans']

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

    awayTeam['aggNotes'] = awayDoc['notes']
    homeTeam['aggNotes'] = homeDoc['notes']

    with open(f"aggNotes/{homeTeam['abbr']}.txt", 'r') as file:
        homeTeam['aggNotes'] = file.read()
    with open(f"aggNotes/{awayTeam['abbr']}.txt", 'r') as file:
        awayTeam['aggNotes'] = file.read()

    # awayTeam['podTrans'] = awayDoc['podTrans']
    # homeTeam['podTrans'] = homeDoc['podTrans']

    awayTeam['depthChart'] = Markup(getNCAADepthHtml(awayDoc['depthChart']))
    homeTeam['depthChart'] = Markup(getNCAADepthHtml(homeDoc['depthChart']))

    # get teams tweets
    awayTeamTwitterList = awayDoc['beat']
    homeTeamTwitterList = homeDoc['beat']
    # awayTeam['tweets'] = getTeamTweets(awayTeamTwitterList)
    # homeTeam['tweets'] = getTeamTweets(homeTeamTwitterList)

    # get podcast and pdf files
    # magazinesFolderPath = '/Users/squeel/magazines/phil/2023/pdfs'
    # magazineFiles = os.listdir(magazinesFolderPath)

    awayTeam["fileNames"] = getTeamTrans(awayTeam['abbr'])
    homeTeam["fileNames"] = getTeamTrans(homeTeam['abbr'])
    # for f in magazineFiles:
    #     if awayTeam['abbr'] in f:
    #         newFileObj = {}
    #         newFileObj['path'] = f"{magazinesFolderPath}/{f}"
    #         newFileObj['title'] = f.split(".")[0]
    #         awayFiles.append(newFileObj)
    #     if homeTeam['abbr'] in f:
    #         newFileObj = {}
    #         newFileObj['path'] = f"{magazinesFolderPath}/{f}"
    #         newFileObj['title'] = f.split(".")[0]
    #         homeFiles.append(newFileObj)

    return render_template('game.html', homeTeam=homeTeam, awayTeam=awayTeam, ngrokDomain=ngrokDomain)

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

@app.route('/trans/<filename>')
def serve_text_file(filename):
    try:
        # with open(os.path.join(transPath, filename), 'r') as file:
        with open("/home/squeel/dev/summy/diarizedTranscripts/workerbee/workerbee-navy.txt", 'r') as file:
            content = file.read()
        
        blue_words = [
            "love",
            "like",
            "pick",
        ]

        red_words = [
            "best bet",
            "lock"
        ]

        green_words = [
            "favorite"
        ]

        # Function to replace words with colored spans
        def highlight_words(content, words, color):
            for word in words:
                content = content.replace(word, f'<span style="color:{color}">{word}</span>')
            return content

        # Highlight the words with different colors
        content = highlight_words(content, blue_words, 'blue')
        content = highlight_words(content, red_words, 'red')
        content = highlight_words(content, green_words, 'green')

        html_content = f'''
        <html>
            <style>
                pre {{
                    white-space: pre-wrap; /* CSS to allow word wrapping */
                    word-wrap: break-word; /* Optional for breaking long words */
                }}
            </style>
        <head>
            <title>{filename}</title>
        </head>
        <body>
            <pre>{content}</pre>
        </body>
        </html>
        '''
        return render_template_string(html_content)
    except FileNotFoundError:
        abort(404)

@app.route('/trans/<path:filename>', methods=['GET'])
def serve_file(filename):
    BASE_DIR = transPath
    # Ensure the file path is safe and within the base directory
    safe_path = os.path.normpath(os.path.join(BASE_DIR, filename))
    if not safe_path.startswith(BASE_DIR):
        return abort(404)  # Prevent directory traversal attacks

    # Get the directory and filename
    directory = os.path.dirname(safe_path)
    file_name = os.path.basename(safe_path)

    if not os.path.exists(safe_path):
        return abort(404)  # File not found

    return send_from_directory(directory, file_name)

if __name__ == '__main__':
    app.run(port=7000, debug=True)