# Pagina12Job.py -- subclase de Job

import datetime
import time
import logging

from Jobs.Job import Job

from Requesters.Pagina12Requester import Pagina12Requester as Requester
from Scrappers.Pagina12Scrapper import Pagina12Scrapper as Scrapper

class Pagina12Job(Job):
    def __init__(self, url = "https://www.pagina12.com.ar/", headers = None, params = None, dbg = False):
        self.name = "Pagina_12"
        self.url = url
        self.headers = headers
        self.params = params
        self.dbg = dbg          # Debugging mode -- False by default. Tags database commmits as "dbg_flag = True"
        print(self.name, self.dbg)
        
        self.primary_key = None			# This signals not ready to commit to database
        self.capture_datetime = None	# This signals not ready to commit to database

        self.requester = Requester(self.url, headers = self.headers, params = self.params, dbg = self.dbg)
        self.scrapper = Scrapper(job_name = self.name, url = self.url, dbg = self.dbg)
        # XXX: does it make sense to pass primary_key & capture_datetime to Scrapper at construction time???
        # XXX: Wouldn't it be better to pass the full requester and allow Scrapper.go_scrape() full freedom
        #      regarding what to scrap as rawdata?