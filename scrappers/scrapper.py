# scrapper.py -- clase general

# este modulo deberia ser solo visible a target

import bs4 as bs
import html5lib
# import html.parser

class scrapper():
    def __init__(self, text):
        self.soup = bs.BeautifulSoup(text, "html5lib")
        # TODO: BeautifulSoup admite varios parsers html/xml
        #       Este hardwireo es medio asqueroso y deberia 
        #       admitir generalizacion que a su vez admita mas
        #       versatilidad al ser usado desde 'target'
        
        
        # self.scraps = None    # Where the scrapped stuff is gonna be 
                                # tucked away in *SOME* representation
                                # still to be well-defined
        # esto no va a estar definido hasta tanto no se tire un go_scrape()

class scrape():
    pass
    # va a hacer las veces de 'bundle' de todo lo que 
    # 'target.store()' tenga que commitear a las databases
    # scrape_raw ===> mongoDB || scrape_raw ===> SQL BLOB/CLOB
    # scrapes ===> SQL // queda por definir un data model 
    