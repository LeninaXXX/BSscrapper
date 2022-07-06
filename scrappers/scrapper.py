# scrapper.py -- clase general

# este modulo deberia ser solo visible a target

import bs4 as bs
import html5lib

class scrapper():
    def __init__(self, text):
        self.soup = bs.BeautifulSoup(text, "html5lib")
        # TODO: BeautifulSoup admite varios parsers html/xml
        #       Este hardwireo es medio asqueroso y deberia 
        #       admitir generalizacion que a su vez admita mas
        #       versatilidad al ser usado desde 'target'
        self.spoils = None  # Where the scrapped stuff is gonna be 
                            # tucked away in *SOME* representation
                            # still to be well-defined