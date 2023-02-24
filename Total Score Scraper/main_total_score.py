from betano_scraper import BetanoScraper
from bwin_scraper import BwinScraper
from data_comparing import DataComparing

betano_data = BetanoScraper().main()
bwin_data = BwinScraper().main()
DataComparing(betano_data, bwin_data)

