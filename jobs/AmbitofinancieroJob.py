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
        
        self.scrapper = Scrapper(self.name, self.requester.payload(), self.primary_key, self.capture_datetime, self.url)
        # TODO: to change to whole requests, and make Scrapper deal with it???
        # TODO: to get rid of passing self.pk_timestamp & self.db_datetime given that those are set at launch() time
        #		It is <target>Job the one in charge of registering the timestamp & primary key
