from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep
import sqlite3

url = "https://www.betano.bg/sport/basketbol/sasht/nba/17106/"

class BetanoScraper():

    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument("start-maximized")

        self.driver = uc.Chrome(options=options)

        self.main()

    def open_page(self):
        self.driver.get(url)

    def get_urls(self):

        urls = []
        i = 2

        while True:

            try:
                url_elem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
                    By.XPATH, f'/html/body/div[1]/div/section[2]/div[5]/div[2]/section/div[4]/div/div/div[2]/table/tr[{i}]/th/a'
                )))
            except:
                break

            i += 1

            # Extract the link from the game element
            link = url_elem.get_attribute('href')

            urls.append(link)

        return urls

    def check_for_bets(self):

        market_headers = WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, "markets__market__header__title"
        )))

        bets_available = False

        for header in market_headers:

            if 'Общо точки (допълнително)' in header.text:
                bets_available = True

        return bets_available

    def get_data(self):

        all_markets = WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, 'markets__market'
        )))

        total_score_market = None

        for market in all_markets:

            if 'Общо точки (допълнително)' in market.text:
                total_score_market = market

        data = total_score_market.text

        return data

    def parse_data(self, data):

        rows = data.split('\n')

        final_data = []

        for row in rows:

            if "Общо точки (допълнително)" in row:
                continue

            if 'Над' in row or 'Под' in row:
                continue

            final_data.append(row)

        return final_data

    def get_teams(self):

        team1_elem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[1]/div/section[2]/div[5]/div[2]/section/div/div[1]/div/div[2]/div/h1/span[1]'
        )))

        team2_elem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[1]/div/section[2]/div[5]/div[2]/section/div/div[1]/div/div[2]/div/h1/span[3]'
        )))

        teams = [team1_elem.text, team2_elem.text]

        return teams

    def form_data(self, score_odds):

        points = None
        i = 0

        for item in score_odds:

            if float(item) > 50 and float(item) == points:
                del score_odds[i]
                points = float(item)

            if float(item) > 50 and float(item) != points:
                points = float(item)

            i += 1

        return score_odds

    def main(self):
        self.open_page()

        urls = self.get_urls()

        betano_data = {}

        for link in urls:

            self.driver.get(link)

            bet_available = self.check_for_bets()

            if bet_available == False:
                continue

            team_names = self.get_teams()

            data = self.get_data()

            score_odds = self.parse_data(data)

            self.form_data(score_odds)

            betano_data[f"{team_names[0]}-{team_names[1]}"] = score_odds

def start():
    scraper = BetanoScraper()


if "__main__" == __name__:
    start()