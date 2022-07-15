# AmbitofinancieroJob.py -- subclase de Job

import datetime
import time

from Jobs.Job import Job

from Requesters.AmbitofinancieroRequester import AmbitofinancieroRequester as Requester
from Scrappers.AmbitofinancieroScrapper import AmbitofinancieroScrapper as Scrapper

class AmbitofinancieroJob(Job):
    def __init__(self, url = "https://www.ambito.com", headers = None, params = None):
        self.name = "Ambito_Financiero"
        self.url = url
        self.headers = headers
        self.params = params
        self.datetime = None    # 'timestamp' a definirse al momento de lanzar el job
                                # lo define self.launch() en la superclase
