# ClarinScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
import re

class ClarinScrapper(Scrapper):    
    def go_scrape(self, ret):
        # First, tuck away raw data:
        soup = bs.BeautifulSoup(ret.text, 'lxml')
       
        for discard_tag in ("script", "style"):
            for t in soup.find_all(discard_tag): t.extract()

        pruned_text = str(soup)
        self.scraps.set_rawdata(ret, pruned_text)