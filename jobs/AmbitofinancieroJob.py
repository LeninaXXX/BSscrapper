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
        self.pk_timestamp = None    # absurdly precise timestamp, to be used as a PRIMARY KEY
        self.db_datetime = None     # properly formatted datetime for the database
        # this data get's defined at Job.launch() time
        # for now, this get to be passed to Scrapper's constructor just 
        # as a placeholder but they remain undefined until launch time

        self.requester = Requester(self.url, headers = self.headers, params = self.params)
        self.scrapper = Scrapper(self.requester.payload_text(), self.pk_timestamp, self.db_datetime, self.name, self.url)
        # TODO: to change to whole requests, and make Scrapper deal with it???
        # TODO: to get rid of passing self.pk_timestamp & self.db_datetime given that those are set at launch() time