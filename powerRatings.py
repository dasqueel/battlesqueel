from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup

def kelly():
    url = "https://kfordratings.com/power"
    webdriver_service = Service(f"chromedriver-linux64/chromedriver")

    chrome_options = Options()
    chrome_options.binary_location = f"chrome-linux64/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Authorization": "Bearer your_api_token",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
    })

    driver.get(url)
    iframe = driver.find_element("tag name", "iframe")
    driver.switch_to.frame(iframe)
    iframe_html = driver.page_source

    driver.switch_to.default_content()
    soup = BeautifulSoup(iframe_html, 'html.parser')
    trs = soup.find_all('tr')
    teamRatings = []
    for tr in trs:
        tds = tr.find_all('td')
        team = tds[1]
        rating = tds[2]
        teamText = team.get_text()
        ratingText = rating.get_text()

        if teamText and ratingText:
            teamRatings.append(
                {"team":teamText, "rating":ratingText}
            )

    driver.quit()
    return teamRatings

if __name__ == "__main__":
    ratings = kelly()
    for rating in ratings: print(rating)