# lanacion_target.py -- subclase de target

from targets.target import target

from requesters.lanacion_requester import lanacion_requester as requester
from scrappers.lanacion_scrapper import lanacion_scrapper as scrapper

class lanacion_target(target):
    def __init__(self, url = "https://www.lanacion.com.ar", header = None, params = None):
        self.url = url
        self.requester = requester(url)   # requester is lanacion_requester 'imported as'...
        self.scrapper = scrapper(self.requester.payload_text())       # scrapper is lanacion_scrapper 'imported as'...

    def launch(self):   # launch'ear el trabajo de requesting + scrapping
        pass            # ... es competecia de este metodo operar requester y al scrapper
                        # ... y lidiar con las sutilezas de esa tarea
    
    def store(self):    # store'ar en la database lo que sea que se obtuvo
        pass