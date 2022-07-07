# lanacion_scrapper.py -- subclase de scrapper

from scrappers.scrapper import scrapper # make superclass visible

import bs4 as bs
import html5lib

class lanacion_scrapper(scrapper):
	# In here, everything should be in reference to the 'self.soup' 
    # belonging to the superclass. The methods particular to this
    # subclass is where the freedom to scrap particular stuff should lie,
    # i.e.: this is pressuambly gonna be where most of the maintenance
    # tasks will lie in the future
    
    # ##################################################################################################################
    # +++ ACA ES DONDE SUCEDE LA MAGIA...
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
    
    
    # Este metodo va a proveer accesso a la representacion piola del scrape
    # (por representacion piola se entiende una que 'calque' el data model de la database)
    # ... no veo razon para que la representacion interna del scrap 
    #     en la clase/instancia no sea ya la 'representacion piola'
    def payload(self):
        try:                    # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
            return self.scraps  # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
        except:                 # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
            self.go_scrape()    # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
            return self.scraps  # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
    
    # esto esta mostly con fines de debugging, para ver si el scrapper 
    # esta (valga la redundancia...) scrappeando lo que yo quiero
    def payload_as_text(self):
        try:
            return self.scraps.__repr__()   # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
        except:                             # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
            self.go_scrape()                # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
            return self.scraps.__repr__()   # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
        # TODO: Aun para fines de debugging, JSON es la que va...
            