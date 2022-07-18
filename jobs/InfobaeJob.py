# InfobaeJob.py -- subclase de Job

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
        
        self.pk_timestamp = None    # absurdly precise timestamp, to be used as a PRIMARY KEY
        self.db_datetime = None     # properly formatted datetime for the database

        self.requester = Requester(self.url, headers = self.headers, params = self.params)
        self.scrapper = Scrapper(self.requester.payload_text(), self.pk_timestamp, self.db_datetime, self.name, self.url)
        # TODO: to change to whole requests, and make Scrapper deal with it???
        # TODO: to get rid of passing self.pk_timestamp & self.db_datetime given that those are set at launch() time
        #		It is <target>Job the one in charge of registering the timestamp & primary key
