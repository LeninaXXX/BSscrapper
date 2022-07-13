# infobae_job.py -- subclase de job

import datetime
import time

from jobs.job import job

from requesters.infobae_requester import infobae_requester as requester
from scrappers.infobae_scrapper import infobae_scrapper as scrapper

class infobae_job(job):
    def __init__(self, url = "https://www.infobae.com", headers = None, params = None):
        self.name = "Infobae"
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
