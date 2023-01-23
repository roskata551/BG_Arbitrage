from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import sqlite3

url = "https://www.betano.bg/sport/basketbol/sasht/nba/17106/"


class BetanoScraper:

    def __init__(self, driver):

        self.driver = driver

        # Creates a connection with the database
        self.con = sqlite3.connect("NBA.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        self.main()

    def get_url(self):
        # Open the url
        self.driver.get(url)

    def get_data(self):

        # Scrape the game element
        teams = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME,
            f'events-list__grid__info__main__participants__participant-name'
        )))

        odds = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME,
            f'selections__selection__odd'
        )))

        return teams, odds

    def parse_data(self, teams, odds):

        games_list = []
        game = []
        i = 0

        for (team, odd) in zip(teams, odds):
            i += 1

            if i % 2 == 1:
                str_team = team.get_attribute('innerText')
                str_odd = odd.get_attribute('innerText')

                game = [str_team, str_odd]
            else:
                str_team = team.get_attribute('innerText')
                str_odd = odd.get_attribute('innerText')

                game.insert(1, str_team)
                game.insert(3, str_odd)
                games_list.append(game)

        return games_list

    def update_database(self, games_list):

        # Deletes the table if it exists
        self.cur.execute("""DROP TABLE IF EXISTS betano_games""")

        # Creates a table if it doesnt exists and makes a place to store the names
        self.cur.execute("""CREATE TABLE IF NOT EXISTS betano_games(
        team_1 TEXT PRIMARY KEY,
        team_2 TEXT,
        odd_1 REAL,
        odd_2 REAL
        )""")

        for game in games_list:

            # Inserts the game data to the database
            self.cur.execute("""INSERT OR IGNORE INTO betano_games VALUES(?,?,?,?)""",
                             game)

        # Commits the connection and saves them
        self.con.commit()

    def main(self):
        self.get_url()

        teams, odds = self.get_data()

        games_list = self.parse_data(teams, odds)

        self.update_database(games_list)


def start():
    scraper = BetanoScraper()

if "__main__" == __name__:
    start()
