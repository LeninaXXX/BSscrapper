# ambitofinanciero_job.py -- subclase de job

import datetime
import time

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
