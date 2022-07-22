# LanacionJobs.py -- subclase de Jobs

import datetime
import time

from Jobs.Job import Job

from Requesters.LanacionRequester import LanacionRequester as Requester
from Scrappers.LanacionScrapper import LanacionScrapper as Scrapper

class LanacionJob(Job):
    def __init__(self, url = "https://www.lanacion.com.ar/", headers = None, params = None):
        self.name = "La_Nacion"
        self.url = url
        self.headers = headers
        self.params = params

        self.pk_timestamp = None    # absurdly precise timestamp, to be used as a PRIMARY KEY
        self.db_datetime = None     # properly formatted datetime for the database

        self.requester = Requester(self.url, headers = self.headers, params = self.params)
        self.scrapper = Scrapper(self.name, self.url, self.primary_key, self.capture_datetime)
		# TODO: to change to whole requests, and make Scrapper deal with it???
        # TODO: to get rid of passing self.pk_timestamp & self.db_datetime given that those are set at launch() time
        #		It is <target>Job the one in charge of registering the timestamp & primary key
