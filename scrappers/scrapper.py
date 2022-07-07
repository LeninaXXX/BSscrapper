# scrapper.py -- clase general

# este modulo deberia ser solo visible a target

import bs4 as bs
import html5lib 

class scrapper():
    def __init__(self, text):
        self.soup = bs.BeautifulSoup(text, "html5lib")
        # TODO: BeautifulSoup admite varios parsers html/xml
        # Este hardwireo es medio asqueroso y deberia admitir generalizacion 
        # que a su vez admita mas versatilidad al ser usado desde 'target'
       
        # self.scraps = None    # Where the scrapped stuff is gonna be 
                                # tucked away in *SOME* representation
                                # still to be well-defined
        # esto no va a estar definido hasta tanto no se tire un go_scrape()

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

class scrape():
    pass
    # va a hacer las veces de 'bundle' de todo lo que 
    # 'target.store()' tenga que commitear a las databases
    # scrape_raw ===> mongoDB || scrape_raw ===> SQL BLOB/CLOB
    # scrapes ===> SQL // queda por definir un data model 

