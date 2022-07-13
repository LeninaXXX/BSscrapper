# lanacion_jobs.py -- subclase de jobs

import datetime
import time

from jobs.job import job

from requesters.lanacion_requester import lanacion_requester as requester
from scrappers.lanacion_scrapper import lanacion_scrapper as scrapper

class lanacion_job(job):
    def __init__(self, url = "https://www.lanacion.com.ar", headers = None, params = None):
        self.name = "La_Nacion"
        self.url = url
        self.headers = headers
        self.params = params
        # self.requester = requester(url)                         # requester is lanacion_requester 'imported as'...
        # self.scrapper = scrapper(self.requester.payload_text()) # scrapper is lanacion_scrapper 'imported as'...

    # launch'ear el trabajo de requesting + scrapping
    # ... es competecia de este metodo operar requester y al scrapper
    # ... y lidiar con las sutilezas de esa tarea
    def launch(self):
        self.uid_timestamp = datetime.datetime.now()
        self.sql_datetime = time.strftime('%Y-%m-%d %H:%M:%S')  

        print("Requesteando...")
        self.requester = requester(self.url, headers = self.headers, params = self.params)
        self.requester.go_fetch()
        
        print("Scrapeando...")
        self.scrapper = scrapper(self.requester.payload_text())
        self.scrapper.go_scrape()

    # store'ar en la database lo que sea que se obtuvo
#   def store(self):
#       # ya se vera...
#       # but this is gonna refer to self.scrapper.payload(), where the scrape is 
#       # represented en un formato confortable a la insercion en una database (un {} ?)
#       
#       print("Mostrar scrape...")
#       print("Storear el request crudo (as it is in self.requester.payload_text()) en MongoDB for future reference?")
#       print("Agarrar la representacion 'piola' (un dictionary?) self.scrapper.payload() e insertarla en SQL?")
#       pass