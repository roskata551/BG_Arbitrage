from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import sqlite3

url = "https://sports.bwin.com/bg/sports/%D0%B1%D0%B0%D1%81%D0%BA%D0%B5%D1%82%D0%B1%D0%BE%D0%BB-7/%D0%B7%D0%B0%D0%BB%D0%B0%D0%B3%D0%B0%D0%BD%D0%B8%D1%8F/%D0%B5%D0%B2%D1%80%D0%BE%D0%BF%D0%B0-7/%D1%88%D0%B0%D0%BC%D0%BF%D0%B8%D0%BE%D0%BD%D1%81%D0%BA%D0%B0-%D0%BB%D0%B8%D0%B3%D0%B0-%D0%BD%D0%B0-%D1%84%D0%B8%D0%B1%D0%B0-55897"


class BwinScraper:

    def __init__(self, driver):
        self.driver = driver

        # Creates a connection with the database
        self.con = sqlite3.connect("ChampoinsLeague.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        self.main()

    def open_url(self):
        self.driver.get(url)

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
                    By.XPATH, f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[1]/ms-six-pack-event[{i}]/div'
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
                    By.XPATH, f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[2]/ms-six-pack-event[{i}]/div'
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

            # Add the right rows to a list
            game_data = [game_rows[0], game_rows[1], float(game_rows[-2]), float(game_rows[-1])]

            # Add the list with the game data to another list
            games_list.append(game_data)

        return games_list

    def update_database(self, games_list):

        # Deletes the table if it exists
        self.cur.execute("""DROP TABLE IF EXISTS bwin_games""")

        # Creates a table if it doesnt exists and makes a place to store the names
        self.cur.execute("""CREATE TABLE IF NOT EXISTS bwin_games(
        team_1 TEXT PRIMARY KEY,
        team_2 TEXT,
        odd_1 REAL,
        odd_2 REAL
        )""")

        for game in games_list:

            # Inserts the game data to the database
            self.cur.execute("""INSERT OR IGNORE INTO bwin_games VALUES(?,?,?,?)""",
                             game)

        # Commits the connection and saves them
        self.con.commit()

    def main(self):
        self.open_url()

        games = self.get_data()

        games_list = self.parse_data(games)

        self.update_database(games_list)

def start():
    scraper = BwinScraper()


if "__main__" == __name__:
    start()
