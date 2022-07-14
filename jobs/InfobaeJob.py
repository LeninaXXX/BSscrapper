# infobae_job.py -- subclase de job

import datetime
import time

from Jobs.Job import Job

from Requesters.InfobaeRequester import InfobaeRequester as Requester
from Scrappers.InfobaeScrapper import InfobaeScrapper as Scrapper

class InfobaeJob(Job):
    def __init__(self, url = "https://www.infobae.com", headers = None, params = None):
        self.name = "Infobae"
        self.url = url
        self.headers = headers
        self.params = params
