# AmbitofinancieroScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
    
class AmbitofinancieroScrapper(Scrapper):   
    def go_scrape(self, ret):
        # First, tuck away raw data:
        self.scraps.set_rawdata(ret)

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