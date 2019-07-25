import requests
import os
import sys
from pipes import quote

school = sys.argv[1]

url = 'https://battlesqueel.herokuapp.com/radio/' + school
r = requests.get(url)
json = r.json()
stations = json['radio']

if len(stations) > 0:
  for i, station in enumerate(stations): print(i, station)

  selection = int(input('select a station: '))

  school = sys.argv[1]
  titleCmd = '"\\033]0;"'+ school +'"\\007"'
  args = ['-ne', titleCmd]
  cmd = 'echo %s' % (' '.join(quote(arg) for arg in args))

  os.system(cmd)
  os.system('mplayer ' + stations[selection])
else:
  print('couldnt play radio station')