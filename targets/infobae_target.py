# infobae_target.py -- subclase de target

from targets.target import target

from requesters.infobae_requester import infobae_requester as requester
from scrappers.infobae_scrapper import infobae_scrapper as scrapper

class infobae_target(target):
    def __init__(self, url = "https://www.infobae.com"):
        self.url = url
        self.headers = headers
        self.params = params
        
    def launch(self):
        print("Requesteando...")
        self.requester = requester(self.url, headers = self.headers, params = self.params)
        self.requester.go_fetch()
        
        print("Scrapeando...")
        self.scrapper = scrapper(self.requester.payload_text())
        self.scrapper.go_scrape()
        
                        
    
    # store'ar en la database lo que sea que se obtuvo
    def store(self):
        # ya se vera...
        # but this is gonna refer to self.scrapper.payload(), where the scrape is 
        # represented en un formato confortable a la insercion en una database (un {} ?)
        
        print("Mostrar scrape...")
        print("Storear el request crudo (as it is in self.requester.payload_text()) en MongoDB for future reference?")
        print("Agarrar la representacion 'piola' (un dictionary?) self.scrapper.payload() e insertarla en SQL?")
        pass
    