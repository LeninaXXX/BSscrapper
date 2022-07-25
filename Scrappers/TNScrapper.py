# TNScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
import re
import logging

class TNScrapper(Scrapper):    
    def go_scrape(self, ret):
        # First, tuck away raw data:
        soup = bs.BeautifulSoup(ret.text, 'lxml')
        beg_size = len(str(soup))
       
        for discard_tag in ("script", "style"):
            for t in soup.find_all(discard_tag): t.extract()

        pruned_text = str(soup)
        end_size = len(pruned_text)

        print(self.name + " | end_size :: ", end_size)
        logging.info(self.name + " | end_size :: " + str(end_size))
        print(self.name + " | beg_size :: ", beg_size)
        logging.info(self.name + " | beg_size :: " + str(beg_size))
        try:
            print(self.name + " | % saving :: ", (beg_size - end_size)/beg_size * 100)
            logging.info(self.name + " | % saving :: " + str((beg_size - end_size)/beg_size * 100))
        except ZeroDivisionError:
            print('ZeroDivisionError Exception -- Presume empty request or request failure')
            logging.error('ZeroDivisionError Exception -- Presume empty request or request failure')
        print('-' * 60)
        self.scraps.set_rawdata(ret, pruned_text)