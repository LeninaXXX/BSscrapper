# Scrapper.py -- general superclass

# this module should only be visible to Job.py

from Scrappers.Articles import Article
from Scrappers.Articles import MainArticle
from Scrappers.Scraps.Scraps import Scraps

from typing import OrderedDict

class Scrapper():
    def __init__(self, job_name, url, primary_key = None, capture_datetime = None):
        
        self.scraps = Scraps(job_name = job_name,
							 primary_key = primary_key, 		# at this point, primary_key nor capture_datetime are set.
							 capture_datetime = capture_datetime)	# at this point, primary_key nor capture_datetime are set.
																# it's done at job.launch() time
        self.scraps.set_url(url)    # FIXME: this should be set at construction time
	
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