# AmbitofinancieroScrapper.py -- subclase de Scrapper

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import html5lib

    # In here, everything should be in reference to the 'self.soup' belonging to the superclass. The methods particular 
    # to this subclass is where the freedom to scrap particular stuff should lie, 
    # i.e.: this is pressuambly gonna be where most of the maintenance tasks will lie in the future
class AmbitofinancieroScrapper(Scrapper):   

    # _Dry Run_ para chequear buen funcionamiento del datamodel e insercion en database  
    def go_scrape(self):

        # make some articles
        article_main = MainArticle("Titulo article_1", "/Economics/href_article_1", "Economics", "Lorem ipsum")
        article_1 = Article("Titulo article_1", "/Politics/href_article_1", "Politics", "Lorem ipsum")
        article_2 = Article("Titulo article_2", "/Society/href_article_2", "Society", "Lorem ipsum")
        article_3 = Article("Titulo article_3", "/Sports/href_article_3", "Sports", "Lorem ipsum")
        article_4 = Article("Titulo article_4", "/Police/href_article_4", "Police", "Lorem ipsum")
        article_5 = Article("Titulo article_4", "/Other/href_article_5", "Other", "Lorem ipsum")

        # Articulo principal
        self.Scraps.add_main_article(article_main)

        # Agrego un articulo
        self.Scraps.add_article(article_1)
        
        # Appendeo unos cuantos
        article_list = [article_2, article_3, article_4, article_5]
        self.Scraps.append_articles(article_list)
