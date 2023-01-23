from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import sqlite3

url = "https://inbet.com/sports/basketball-1002/champions-league-19000014051?group=100219&tab=matches"


class InbetScraper:

    def __init__(self, driver):
        self.driver = driver

        # Creates a connection with the database
        self.con = sqlite3.connect("ChampoinsLeague.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        self.main()

    def get_url(self):
        # Open the url
        self.driver.get(url)

        self.driver.refresh()

    def get_data(self):

        # Variable to count the game wich is scraped
        i = 0
        # List for the scraped data
        games = []

        while True:

            i += 1

            try:
                # Scrape the game element
                game = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, f'#root > div.main-content > main > div > div.content.no-scrollbars > div > div.block--league-markets > div:nth-child(1) > div.group > div:nth-child({i})'
                )))

                # Add the game raw data to the list
                games.append(game.text)
            except:
                break


        # Variable to count the game wich is scraped
        i = 0

        while True:

            i += 1

            try:
                # Scrape the game element
                game = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, f'#root > div.main-content > main > div > div.content.no-scrollbars > div > div.block--league-markets > div:nth-child(2) > div.group > div:nth-child({i})'
                )))

                # Add the game raw data to the list
                games.append(game.text)
            except:
                break

        return games

    def parse_data(self, games):

        # List for the game data
        games_list = []

        for game in games:

            # Split the raw data in to rows
            game_rows = game.split("\n")

            if len(game_rows) > 16:
                game_rows.pop()

            # Add the right rows to a list
            game_data = [game_rows[0], game_rows[1], float(game_rows[-3]), float(game_rows[-1])]

            # Add the list with the game data to another list
            games_list.append(game_data)

        return games_list

    def update_database(self, games_list):

        # Deletes the table if it exists
        self.cur.execute("""DROP TABLE IF EXISTS inbet_games""")

        # Creates a table if it doesnt exists and makes a place to store the names
        self.cur.execute("""CREATE TABLE IF NOT EXISTS inbet_games(
        team_1 TEXT PRIMARY KEY,
        team_2 TEXT,
        odd_1 REAL,
        odd_2 REAL
        )""")

        for game in games_list:

            # Inserts the game data to the database
            self.cur.execute("""INSERT OR IGNORE INTO inbet_games VALUES(?,?,?,?)""",
                             game)

        # Commits the connection and saves them
        self.con.commit()

    def main(self):
        self.get_url()

        games = self.get_data()

        games_list = self.parse_data(games)

        self.update_database(games_list)


def start():
    scraper = InbetScraper()

if "__main__" == __name__:
    start()
