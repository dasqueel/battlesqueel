'''

contestSlot Object

could have multiple saved drafts for a contestSlot

read from csv file
  * contains all players
  * creates a mongo doc for that csv which hold mutated state from user
    * removed players, num of lineups, allocations of each player, etc...

write a new csv file to upload
order the lineups by salary left over

def generateLineups(csvFile, numOfLineups)

OBJECTS

contestSlot
  * csvFile string
  * numOfLineups int
  * lineups [<lineUp>]
  * site enum ['dk', 'fd']

METHODS

returns an array of lineup objects
csvToJson(csvFile)

void creates a new csv file
jsonToCsv(json)

'''