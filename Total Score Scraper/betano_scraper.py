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
        # Creates a connection with the database
        self.con = sqlite3.connect("Arbitrage.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        options = webdriver.ChromeOptions()

        options.add_argument("start-maximized")

        self.driver = uc.Chrome(options=options)

    def open_page(self):
        self.driver.get(url)

    def get_urls(self):

        urls = []
        i = 2

        while True:

            try:
                url_elem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
                    By.XPATH, f'/html/body/div[1]/div/section[2]/div[4]/div[2]/section/div[4]/div/div/div[2]/table/tr[{i}]/th/a'
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
            By.XPATH, '/html/body/div[1]/div/section[2]/div[4]/div[2]/section/div/div[1]/div/div[2]/div/h1/span[1]/span/span'
        )))

        team2_elem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div[1]/div/section[2]/div[4]/div[2]/section/div/div[1]/div/div[2]/div/h1/span[3]/span/span'
        )))

        teams = [team1_elem.text, team2_elem.text]

        return teams

    def form_data(self, score_odds):

        dic = {}

        i = 0
        score = None
        for item in score_odds:

            i += 1

            if i == 1:
                dic[item] = []
                score = item

            elif i == 2:
                dic[score].append(item)

            elif i == 3:
                continue

            elif i == 4:
                dic[score].append(item)
                i = 0

        return dic

    def get_name_dict(self):
        # Selects the table with the site name
        self.cur.execute(f"""SELECT * FROM name_dictionary""")

        # Gets all the data from the table
        name_dict = self.cur.fetchall()

        return name_dict

    def change_names(self, names, name_dict):

        for ls in name_dict:

            if names[0] in ls:
                names[0] = ls[0]

            if names[1] in ls:
                names[1] = ls[0]

        return names

    def main(self):
        self.open_page()

        urls = self.get_urls()

        name_dict = self.get_name_dict()

        betano_data = {}

        for link in urls:

            self.driver.get(link)

            bet_available = self.check_for_bets()

            if bet_available == False:
                continue

            team_names = self.get_teams()

            data = self.get_data()

            score_odds = self.parse_data(data)

            score_dic = self.form_data(score_odds)

            new_names = self.change_names(team_names, name_dict)

            betano_data[" vs ".join(new_names)] = score_dic

        return betano_data

def start():
    scraper = BetanoScraper()


if "__main__" == __name__:
    start()