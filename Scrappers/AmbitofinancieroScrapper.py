# AmbitofinancieroScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
import re
import logging
    
class AmbitofinancieroScrapper(Scrapper):   
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







"""
        # Dummy article to test database insertion
                # Build some articles
                    # A MainArticle
        article_main = MainArticle("Headline title", "/Economics/href_headline", "Economics", "Lorem ipsum")
	    			# ... some other articles
        article_1 = Article("Titulo article_1", "/Politics/href_article_1", "Politics", "Lorem ipsum")
        article_2 = Article("Titulo article_2", "/Society/href_article_2", "Society", "Lorem ipsum")
        article_3 = Article("Titulo article_3", "/Sports/href_article_3", "Sports", "Lorem ipsum")
        article_4 = Article("Titulo article_4", "/Police/href_article_4", "Police", "Lorem ipsum")
        article_5 = Article("Titulo article_4", "/Other/href_article_5", "Other", "Lorem ipsum")
	    		# add main article
        self.scraps.add_main_article(article_main)
	    		# ... add an article
        self.scraps.add_article(article_1)
	    		# ... append some articles
        
        article_list = [article_2, article_3, article_4, article_5]
        self.scraps.append_articles(article_list)
"""