import csv

qbId = ''
rb1Id = ''
rb2Id = ''
wr1Id = ''
wr2Id = ''
flexId = ''
sFlexId = ''

with open("csv/dkout.csv", "wb") as f:
  writer = csv.writer(f)
  writer.writerow(["QB", "RB", "RB","WR","WR","WR","FLEX","S-FLEX"])
  writer.writerows(idLineups)