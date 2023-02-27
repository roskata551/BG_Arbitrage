from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep
import sqlite3

url = "https://sports.bwin.com/bg/sports/%D0%B1%D0%B0%D1%81%D0%BA%D0%B5%D1%82%D0%B1%D0%BE%D0%BB-7/%D0%B7%D0%B0%D0%BB%D0%B0%D0%B3%D0%B0%D0%BD%D0%B8%D1%8F/%D1%81%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D0%B0-%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0-9/%D0%BD%D0%B1%D0%B0-6004"


class BwinScraper:

    def __init__(self):
        # Creates a connection with the database
        self.con = sqlite3.connect("Arbitrage.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        options = webdriver.ChromeOptions()

        options.add_argument("start-maximized")

        self.driver = uc.Chrome(options=options)

    def find_by_text(self, elements, text):
        # A function for finding an element with specific text in it

        result = None

        for elem in elements:

            if text in elem.text:
                result = elem

        return result

    def find_sub_elements(self, element, tag_name):
        # A function for finding sub elements with specific tag name

        result = element.find_elements(By.TAG_NAME, tag_name)

        return result

    def open_url(self):
        self.driver.get(url)

    def get_links(self):

        # Variable to count the game wich is scraped
        i = 0
        # List for the scraped data
        games_links = []

        while True:

            i += 1

            try:
                # Find the game element with the link in it
                game_elem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[{i}]/div/a'
                )))

                # Extract the link from the game element
                link = game_elem.get_attribute('href')

                # Add the link to a list
                games_links.append(link)
            except:
                break

        # Variable to count the game wich is scraped
        i = 0

        while True:

            i += 1

            try:
                # Find the game element for the second day with the link in it
                game_elem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[2]/ms-six-pack-event[{i}]/div/a'
                )))

                # Extract the link from the game element
                link = game_elem.get_attribute('href')

                # Add the link to a list
                games_links.append(link)
            except:
                break

        return games_links

    def check_for_bets(self):

        # Variable for the amount of data in the page
        data_quantity = 0

        bets_available = False

        try:
            # Find the element for the menu in wich are shown all the bets ant click it
            all_menus = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((
                By.TAG_NAME,
                'li'
            )))

            total_score_menu = self.find_by_text(all_menus, "Общ резултат")

            total_score_menu.click()

            # If the element is not found the amount of data is still zero
        except:
            return bets_available

        # Find an element for all the bets in the menu
        bets_elem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
            By.TAG_NAME,
            'ms-option-group-list'
        )))

        # The amount of data equals the amount of text in the menu
        data_quantity = len(bets_elem.text)

        # If the amount of data is more than 1200 bets are available
        if data_quantity > 400:

            bets_available = True

        return bets_available

    def get_team_names(self):
        # Find the name of the teams
        team_name_elems = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((
            By.TAG_NAME, 'ms-scoreboard-participant'
        )))

        team_names = []

        for team_name_elem in team_name_elems:

            team_names.append(team_name_elem.text)

        return team_names

    def get_total_score_odds(self):

        # Finds the menu for the total score bets
        menu_elem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="main-view"]/ng-component/div/ms-option-group-list/div[1]/ms-option-panel[1]'
        )))

        # Finds the elements with "div" tag because there is the show more button
        menu_sub_elems = self.find_sub_elements(menu_elem, "div")

        # Finding the element for the show more button
        show_more_button = self.find_by_text(menu_sub_elems, "Покажи повече")
        show_more_button.click()

        # Finds the menu for the total score bets again after it was expanded
        menu_elem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="main-view"]/ng-component/div/ms-option-group-list/div[1]/ms-option-panel[1]'
        )))

        # Splits the text in to rows
        odds = menu_elem.text.split("\n")

        # Adds only the rows needed
        del odds[0:6], odds[-1]

        return odds

    def form_data(self, score_odds):

        dic = {}

        i = 0
        score = None
        for item in score_odds:
            i += 1

            if i == 1:
                comma_score = item
                score = comma_score.replace(",", ".")
                dic[score] = []

            elif i == 2:
                dic[score].append(item)

            elif i == 3:
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

        self.open_url()

        # Maximizes the window to fit all the menus inside
        self.driver.maximize_window()

        # Gets a list of urls for the games
        links = self.get_links()

        name_dict = self.get_name_dict()

        bwin_data = {}

        # Goes trough every link from the list
        for link in links:

            self.driver.get(link)

            # Checks if there are any bets available
            bets_available = self.check_for_bets()

            if bets_available == False:
                continue

            team_names = self.get_team_names()

            try:
                total_score_odds = self.get_total_score_odds()
            except:
                continue

            dic = self.form_data(total_score_odds)

            new_names = self.change_names(team_names, name_dict)

            bwin_data[" vs ".join(new_names)] = dic

        return bwin_data


def start():
    scraper = BwinScraper()


if "__main__" == __name__:
    start()
