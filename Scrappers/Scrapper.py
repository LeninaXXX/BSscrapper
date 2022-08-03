# Scrapper.py -- general superclass

# this module should only be visible to Job.py

from Scrappers.Articles import Article
from Scrappers.Articles import MainArticle
from Scrappers.Scraps.Scraps import Scraps

class Scrapper():
    # job_name & url : need to be known at build time
    # primary_key & capture_datetime : generated only at launchtime
    def __init__(self, job_name, url, primary_key = None, capture_datetime = None, dbg = False):
        self.name = job_name
        self.url = url
        self.primary_key = primary_key
        self.capture_datetime = capture_datetime
        self.dbg = dbg
        print("Scrapper :", self.name, self.dbg)

        self.scraps = Scraps(job_name = self.name,
                             url = self.url, 
							 primary_key = self.primary_key, 		    # at this point, primary_key nor capture_datetime are set.
							 capture_datetime = self.capture_datetime,
                             dbg = self.dbg
                            )	# at this point, primary_key nor capture_datetime are set.
																    # it's done at job.launch() time
        # self.scraps.set_url(url)
        # FIXED: Check for fix -- url should be set at build time

    def set_primary_key(self, primary_key):
        # print("+++PRIMARY KEY SET ::", primary_key)
        self.scraps.set_primary_key(primary_key)
		
    def set_capture_datetime(self, capture_datetime):
        # print("+++CAPTURE DATETIME SET ::", capture_datetime)
        self.scraps.set_capture_datetime(capture_datetime)
    
    def get_MongoDB_raw_scraps_as_dict(self):
        return self.scraps.scraps_MongoDB.raw_as_dict()     # FIXME: this seems inelegant
    
    def get_MongoDB_clean_scraps_as_dict(self):
        return self.scraps.scraps_MongoDB.clean_as_dict()   # FIXME: this seems inelegant. I'm accessing something buried
                                                            #        it's self.scraps the one that should be exposing methods to allow access
    def get_SQL_scraps_as_dict(self):   
        return self.scraps.scraps_SQL.as_dict()             # FIXME: same deal...