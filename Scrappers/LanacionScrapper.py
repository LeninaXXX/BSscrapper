# LanacionScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
import re

class LanacionScrapper(Scrapper):    
    def go_scrape(self, ret):
        # First, tuck away raw data:
        soup = bs.BeautifulSoup(ret.text, 'lxml')
        beg_size = len(str(soup))
       
        for discard_tag in ("script", "style"):
            for t in soup.find_all(discard_tag): t.extract()

        pruned_text = str(soup)
        end_size = len(pruned_text)

        print(self.name + " | beg_size :: ", beg_size)
        print(self.name + " | end_size :: ", end_size)
        print(self.name + " | % saving :: ", (beg_size - end_size)/beg_size * 100)
        self.scraps.set_rawdata(ret, pruned_text)