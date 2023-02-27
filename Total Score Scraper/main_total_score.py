from betano_scraper import BetanoScraper
from bwin_scraper import BwinScraper
from data_comparing import DataComparing

bwin_data = BwinScraper().main()
betano_data = BetanoScraper().main()
DataComparing(betano_data, bwin_data)

