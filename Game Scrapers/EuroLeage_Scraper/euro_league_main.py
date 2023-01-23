from Modules import bet365
from Modules import betano
from Modules import bwin
from Modules import efbet
from Modules import sesame
from Modules import game_sorting
from selenium import webdriver
import undetected_chromedriver as uc

options = webdriver.ChromeOptions()

options.add_argument("start-maximized")

driver = uc.Chrome(options=options)

bet365.Bet365Scraper(driver)
betano.BetanoScraper(driver)
bwin.BwinScraper(driver)
efbet.EfbetScraper(driver)
sesame.SesameScraper(driver)

game_sorting.GameSorting()

