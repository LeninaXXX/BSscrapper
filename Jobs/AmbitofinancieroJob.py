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
        
        self.primary_key = None			# This signals not ready to commit to database
        self.capture_datetime = None	# This signals not ready to commit to database

        self.requester = Requester(self.url, headers = self.headers, params = self.params)
        self.scrapper = Scrapper(job_name = self.name, url = self.url)
        # XXX: does it make sense to pass primary_key & capture_datetime to Scrapper at construction time???
        # XXX: Wouldn't it be better to pass the full requester and allow Scrapper.go_scrape() full freedom
        #      regarding what to scrap as rawdata?
