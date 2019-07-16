from bs4 import BeautifulSoup
import requests


def getDepthHtml(ourLandsAbbr):
	# Create a variable with the URL to this tutorial
	url = 'http://www.ourlads.com/nfldepthcharts/depthchart/'+ourLandsAbbr
	# Scrape the HTML at the url
	r = requests.get(url)

	# Turn the HTML into a Beautiful Soup object
	soup = BeautifulSoup(r.text, 'html.parser')

	table = soup.find(class_='table table-bordered')

	for row in table.find_all('td'):
		try:
			if 'dt-sh' in row.attrs['class']:
				row.extract()
		except:
			pass

	return table

from bs4 import BeautifulSoup
import requests

def getNCAADepthHtml(teamOurLandsUrl):

	# Scrape the HTML at the url
	r = requests.get(teamOurLandsUrl)

	# Turn the HTML into a Beautiful Soup object
	soup = BeautifulSoup(r.text, 'html.parser')

	[s.extract() for s in soup('th')]

	table = soup.find(class_='col-md-12 blog-page')

	links = table.find_all('a')

	for link in links: link['target'] = '_blank'

	return table