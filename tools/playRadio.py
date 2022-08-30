import requests
import os
import sys
from pipes import quote

team = sys.argv[1]

# url = 'https://battlesqueel.herokuapp.com/radio/' + team
url = 'http://127.0.0.1:5000/radio/' + team
r = requests.get(url)
json = r.json()
stations = json['radio']

if len(stations) > 0:
    for i, station in enumerate(stations):
        print(i, station)

    selection = int(input('select a station: '))

    team = sys.argv[1]
    titleCmd = '"\\033]0;"' + team + '"\\007"'
    args = ['-ne', titleCmd]
    cmd = 'echo %s' % (' '.join(quote(arg) for arg in args))

    os.system(cmd)
    os.system('mplayer ' + stations[selection])
else:
    print('couldnt play radio station')
