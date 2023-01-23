from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import undetected_chromedriver as uc
import sqlite3

url = "https://efbet.com"


class EfbetScraper:

    def __init__(self, driver):
        self.driver = driver

        # Creates a connection with the database
        self.con = sqlite3.connect("EuroLeague.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        self.main()

    def open_page(self):
        self.driver.get(url)

        sleep(3)

        # Find and click the basketball button
        basket_button = WebDriverWait(self.driver, 10).until((EC.presence_of_element_located((
            By.XPATH, '//*[@id="AdvSportsNavComponent26-link-281982.1"]/a[1]'))))
        basket_button.click()

    def get_raw_data(self):
        sleep(5)

        # Find the main tab with all the league tabs in it and wait 10 sec for the page to load
        main_tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div[4]/div[3]")))

        # Search for the league tabs within the main tab and save them in a list variable
        league_tabs = main_tab.find_elements(By.CLASS_NAME, 'container')

        # Find the tab with the NBA games
        nba_tab = None

        for league_tab in league_tabs:

            if "Жени" in league_tab.text:
                continue

            if "Евролига" in league_tab.text:
                nba_tab = league_tab

        return nba_tab

    def parse_data(self, nba_tab):

        # Find the game in the NBA tab
        games = nba_tab.find_elements(By.TAG_NAME, "tr")

        games_list = []

        for game in games:

            # Converts the web element to a string and splits it in to rows
            game_rows = game.text.split("\n")

            # If there are more then 3 rows the data is usable
            if len(game_rows) > 3:

                # Splits the string with the teams
                teams = game_rows[2].split(" vs ")

                # Creates a list with the game data
                game_data = [teams[0], teams[1], game_rows[-3], game_rows[-2]]

                games_list.append(game_data)

        return games_list

    def update_database(self, games_list):

        # Deletes the table if it exists
        self.cur.execute("""DROP TABLE IF EXISTS efbet_games""")

        # Creates a table if it doesnt exists and makes a place to store the names
        self.cur.execute("""CREATE TABLE IF NOT EXISTS efbet_games(
        team_1 TEXT PRIMARY KEY,
        team_2 TEXT,
        odd_1 REAL,
        odd_2 REAL
        )""")

        for game in games_list:

            # Inserts the game data to the database
            self.cur.execute("""INSERT OR IGNORE INTO efbet_games VALUES(?,?,?,?)""",
                             game)

        # Commits the connection and saves them
        self.con.commit()

    def main(self):
        self.open_page()

        nba_tab = self.get_raw_data()

        games_list = self.parse_data(nba_tab)

        self.update_database(games_list)


def main():
    scraper = EfbetScraper()


if __name__ == '__main__':
    main()