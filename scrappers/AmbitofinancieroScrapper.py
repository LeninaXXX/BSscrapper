# ambitofinanciero_scrapper.py -- subclase de scrapper

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
    # ##################################################################################################################
    # +++ la magia ... (?)
    # ##################################################################################################################
    # def go_scrape(self):
    #     self.scraps =        { "title" : self.soup.title.string}
    #        
    #     h_main = self.soup.find_all("h1")       # articulo principal    // usualmente 1 \
    #     # h2s = self.soup.find_all("h2")        # articulos secundarios // usualmente 5  \__ total de 6
    #    
    #     article = h_main[0].parent
    #     
    #     titulo_h1 = article.find_all("h1")[0].get_text()
    #     titulo_href = article.find_all("h1")[0].find_all("a")[0]['href']
    #     copete_h2 = article.find_all("h2")[0].get_text()
    #     autor_div = article.find_all("div")[0].get_text()
    # 
    #     self.scraps.update({"titulo_h1"   : titulo_h1}) 
    #     self.scraps.update({"titulo_href" : titulo_href})
    #     self.scraps.update({"copete_h2"   : copete_h2})
    #     self.scraps.update({"autor_div"   : autor_div})    
    # ##################################################################################################################
    
    # dry run. Scrape ficticio para probar las clases del datamodel y su interfaz
    # todavia no esta lista
    def go_scrape(self):
        self.scrape = Scraps()

        article_main = MainArticle("Titulo article_1", "/Economics/href_article_1", "Economics", "Lorem ipsum")
        article_1 = Article("Titulo article_1", "/Politics/href_article_1", "Politics", "Lorem ipsum")
        article_2 = Article("Titulo article_2", "/Society/href_article_2", "Society", "Lorem ipsum")
        article_3 = Article("Titulo article_3", "/Sports/href_article_3", "Sports", "Lorem ipsum")
        article_4 = Article("Titulo article_4", "/Police/href_article_4", "Police", "Lorem ipsum")
        article_5 = Article("Titulo article_4", "/Other/href_article_5", "Other", "Lorem ipsum")

        self.scrape.add_main_article(article_main)

        self.scrape.set_


