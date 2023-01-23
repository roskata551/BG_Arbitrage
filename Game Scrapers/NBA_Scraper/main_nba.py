from Modules import bet365_scraper
from Modules import betano_scraper
from Modules import bwin_scraper
from Modules import efbet_scraper
from Modules import sesame_scraper
from Modules import game_sorting
from selenium import webdriver
import undetected_chromedriver as uc

options = webdriver.ChromeOptions()

options.add_argument("start-maximized")

driver = uc.Chrome(options=options)

# bet365_scraper.Bet365Scraper(driver)
# betano_scraper.BetanoScraper(driver)
# bwin_scraper.BwinScraper(driver)
efbet_scraper.EfbetScraper(driver)
sesame_scraper.SesameScraper(driver)

game_sorting.GameSorting()
