# ambitofinanciero_job.py -- subclase de job

import datetime

from jobs.job import job

from requesters.ambitofinanciero_requester import ambitofinanciero_requester as requester
from scrappers.ambitofinanciero_scrapper import ambitofinanciero_scrapper as scrapper

class ambitofinanciero_job(job):
    def __init__(self, url = "https://www.ambito.com", headers = None, params = None):
        self.name = "Ambito_Financiero"
        self.url = url
        self.headers = headers
        self.params = params
        self.datetime = None    # 'timestamp' a definirse al momento de lanzar el job
                                # lo define self.launch() en la superclase

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