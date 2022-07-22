# RadiomitreScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
import re

class RadiomitreScrapper(Scrapper):    
    def go_scrape(self, ret):
        # tuck away rawdata
        self.scraps.set_rawdata(ret)