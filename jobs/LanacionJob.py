# lanacion_jobs.py -- subclase de jobs

import datetime
import time

from Jobs.Job import Job

from Requesters.LanacionRequester import LanacionRequester as requester
from Scrappers.LanacionScrapper import LanacionScrapper as scrapper

class LanacionJob(Job):
    def __init__(self, url = "https://www.lanacion.com.ar", headers = None, params = None):
        self.name = "La_Nacion"
        self.url = url
        self.headers = headers
        self.params = params
