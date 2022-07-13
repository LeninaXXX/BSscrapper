# lanacion_scrapper.py -- subclase de scrapper

from scrappers.scrapper import scrapper # make superclass visible

import bs4 as bs
import html5lib

    # In here, everything should be in reference to the 'self.soup' belonging to the superclass. The methods particular 
    # to this subclass is where the freedom to scrap particular stuff should lie, 
    # i.e.: this is pressuambly gonna be where most of the maintenance tasks will lie in the future
class lanacion_scrapper(scrapper):    
    # ##################################################################################################################
    # +++ la magia ... (?)
    # ##################################################################################################################
    def go_scrape(self):
        self.scraps =        { "title" : self.soup.title.string}
           
        h_main = self.soup.find_all("h1")       # articulo principal    // usualmente 1 \
        # h2s = self.soup.find_all("h2")        # articulos secundarios // usualmente 5  \__ total de 6
       
        article = h_main[0].parent
        
        titulo_h1 = article.find_all("h1")[0].get_text()
        titulo_href = article.find_all("h1")[0].find_all("a")[0]['href']
        copete_h2 = article.find_all("h2")[0].get_text()
        autor_div = article.find_all("div")[0].get_text()

        self.scraps.update({"titulo_h1"   : titulo_h1}) 
        self.scraps.update({"titulo_href" : titulo_href})
        self.scraps.update({"copete_h2"   : copete_h2})
        self.scraps.update({"autor_div"   : autor_div})
     
    # ##################################################################################################################
