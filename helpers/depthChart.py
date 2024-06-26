from bs4 import BeautifulSoup
import requests
from utils import getPffPlayerObj

def getPlayerYoutubeSearchString(depthChartPlayerName):
    normalName = depthChartPlayerName.split(' ')
    normalName = f"{normalName[1].strip()} {normalName[0][:-1]}"

    return(normalName)

def getNCAADepthHtml(teamOurLandsUrl, teamAbbr, pffTeamName):
	try:
		r = requests.get(teamOurLandsUrl)
		soup = BeautifulSoup(r.text, 'html.parser')

		td_tags = soup.find_all('td')
		playerTdEls = [td for td in td_tags if td.find('a') and ',' in td.find('a').text]

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
			newEl.string = "goog "
			td.append(newEl)

			try:
				pffPlayerObj = getPffPlayerObj(playerName, teamAbbr, pffTeamName)
				gradesToShow = pffPlayerObj['gradesToShow']
				gradesToShowString = ' '.join([f'{key}: {value}' for key, value in gradesToShow.items()]) 
				pffEl = soup.new_tag('span')
				pffEl.string = gradesToShowString
				td.append(pffEl)
			except Exception as e:
				pass

		[s.extract() for s in soup('th')]

		table = soup.find(class_='col-md-12 blog-page')
		
		links = table.find_all('a')

		for link in links: link['target'] = '_blank'

		return table
	except Exception  as e:
		print(e)
		empty_span_html = '<span></span>'
		soup = BeautifulSoup(empty_span_html, 'html.parser')
		return soup