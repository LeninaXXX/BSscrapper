# La100Job.py -- subclase de Job

import datetime

from Jobs.Job import Job

from Requesters.La100Requester import La100Requester as Requester
from Scrappers.La100Scrapper import La100Scrapper as Scrapper

class La100Job(Job):
    def __init__(self, url = "http://la100.cienradios.com/", headers = None, params = None, dbg = False):
        self.job_name = "La_100"
        self.url = url
        self.headers = headers
        self.params = params
        self.dbg = dbg                  # Debugging mode -- False by default. Tags database commmits as "dbg_flag = True"

        # SQL Parameters -- NOTE: 2022-11-10 -- No new fields to be added in this iteration, but try to fill article/cluster
        self.job_sql_table = 'articles_scrap_v2_la_100' if not self.dbg else 'articles_scrap_v2_dbg'

        self.primary_key = None			                # This signals not ready to commit to database
        self.capture_datetime = datetime.datetime.now() # This signals not ready to commit to database

        self.requester = Requester(job_name = self.job_name, url = self.url, headers = self.headers, params = self.params, dbg = self.dbg)
        self.scrapper = Scrapper(job_name = self.job_name, url = self.url, dbg = self.dbg)
        # XXX: does it make sense to pass primary_key & capture_datetime to Scrapper at construction time???
        # XXX: Wouldn't it be better to pass the full requester and allow Scrapper.go_scrape() full freedom
        #      regarding what to scrap as rawdata?