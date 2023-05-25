from bs4 import BeautifulSoup
import requests

def getPlayerYoutubeSearchString(depthChartPlayerName):
    normalName = depthChartPlayerName.split(' ')
    normalName = f"{normalName[1].strip()} {normalName[0][:-1]}"

    return(normalName)

def getNCAADepthHtml(teamOurLandsUrl):

	# Scrape the HTML at the url
	r = requests.get(teamOurLandsUrl)

	# Turn the HTML into a Beautiful Soup object
	soup = BeautifulSoup(r.text, 'html.parser')

	td_tags = soup.find_all('td')

	# Inject player links
	# Filter the td tags based on the presence of 'href' attribute and comma in the text
	playerTdEls = [td for td in td_tags if td.find('a') and ',' in td.find('a').text]

	# Output the filtered td tags
	for td in playerTdEls:
		playerName = td.text.strip()
		playerSearchStr = getPlayerYoutubeSearchString(playerName)

		# add yt search
		newEl = soup.new_tag('a', attrs={"href":f"https://youtube.com/search?q={playerSearchStr} football"})
		newEl.string = "  yt | "
		td.append(newEl)

		# twitter search
		newEl = soup.new_tag('a', attrs={"href":f"https://twitter.com/search?q={playerSearchStr}&f=live"})
		newEl.string = "twit | "
		td.append(newEl)

		# google search
		newEl = soup.new_tag('a', attrs={"href":f"https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&as_qdr=m&q={playerSearchStr} football"})
		newEl.string = "goog"
		td.append(newEl)

		# TODO get pff ranking and 247 rating clicks

	[s.extract() for s in soup('th')]

	table = soup.find(class_='col-md-12 blog-page')
	
	links = table.find_all('a')

	for link in links: link['target'] = '_blank'

	return table