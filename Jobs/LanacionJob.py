# LanacionJobs.py -- Jobs subclass

import datetime

from Jobs.Job import Job

from Requesters.LanacionRequester import LanacionRequester as Requester
from Scrappers.LanacionScrapper import LanacionScrapper as Scrapper

class LanacionJob(Job):
    def __init__(self, url = "https://www.lanacion.com.ar/", headers = None, params = None, dbg = False):
        self.job_name = "La_Nacion"
        self.url = url
        self.headers = headers
        self.params = params
        self.dbg = dbg                  # Debugging mode -- False by default. Tags database commmits as "dbg_flag = True"
        
        # SQL Parameters -- NOTE: 2022-11-10 -- No new fields to be added in this iteration, but try to fill article/cluster
        self.job_sql_table = 'articles_scrap_v2_la_nacion' if not self.dbg else 'articles_scrap_v2_dbg'

        self.primary_key = None			                # This signals not ready to commit to database
        self.capture_datetime = datetime.datetime.now() # This signals not ready to commit to database

        self.requester = Requester(job_name = self.job_name, url = self.url, headers = self.headers, params = self.params, dbg = self.dbg)
        self.scrapper = Scrapper(job_name = self.job_name, url = self.url, dbg = self.dbg)
        # XXX: does it make sense to pass primary_key & capture_datetime to Scrapper at construction time???
        # XXX: Wouldn't it be better to pass the full requester and allow Scrapper.go_scrape() full freedom
        #      regarding what to scrap as rawdata?