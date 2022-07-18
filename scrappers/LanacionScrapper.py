# LanacionScrapper.py -- subclase de Scrapper

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml

class LanacionScrapper(Scrapper):    
    def go_scrape(self):
		self.scraps = Scraps()
