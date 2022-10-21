from typing import OrderedDict

class ScrapsSQL():
    def __init__(self, job_name = None, url = None, primary_key = None, capture_datetime = None, dbg = False):
        # SQL DataModel
        self.SQL_row = OrderedDict({    # Explicitly OrderedDict(), even if dict() is ordered by default
            "id" : primary_key,						# PRIMARY KEY : name + timestamp @ job launch time
            "jobName" : job_name,                   # Name of the target (e.g.: La_Nacion)
            "captureDatetime" : capture_datetime,   # datetime @ job launch time
            "url" : url,                           # ACTUAL url being scrapped 
            
            "mainArticleTitle" : None,      		# 
            "mainArticleHref" : None,       		# relative url of main article
            "mainArticleCategory" : None,   		# category as infered (e.g.: from slug)
					
            "nArticles" : 0,                		# number of articles
            "nEconomics" : 0,               		# number of articles in the category of 'economics'
            "nPolitics" : 0,                		# ... politics
            "nSociety" : 0,                 		# ... society
            "nSports" : 0,                  		# ... sports
            "nPolice" : 0,                  		# ... police
            "nOthers" : 0                   		# number on a category not known in advance
        })
        if dbg:     # if called in debug mode, tag database commit
            self.set_debug_flag()

    def set_debug_flag(self):
        self.SQL_row["DBG_FLAG"] = True
    
    def set_primary_key(self, primary_key):
        self.SQL_row["id"] = primary_key
    def set_capture_datetime(self, capture_datetime):
        self.SQL_row["captureDatetime"] = capture_datetime
        
    def set_name(self, name):
        self.SQL_row["jobName"] = name
    def set_url(self, url):
        self.SQL_row["url"] = url

    def set_mainArticleTitle(self, mainArticleTitle):
        self.SQL_row["mainArticleTitle"] = mainArticleTitle
    def set_mainArticleHref(self, mainArticleHref):
        self.SQL_row["mainArticleHref"] = mainArticleHref
    def set_mainArticleCategory(self, mainArticleCategory):
        self.SQL_row["mainArticleCategory"] = mainArticleCategory

    def set_nArticles(self, nArticles):
        self.SQL_row["nArticles"] = nArticles
    def set_nEconomics(self, nEconomics):
        self.SQL_row["nEconomics"] = nEconomics
    def set_nPolitics(self, nPolitics):
        self.SQL_row["nPolitics"] = nPolitics
    def set_nSociety(self, nSociety):
        self.SQL_row["nSociety"] = nSociety
    def set_nSports(self, nSports):
        self.SQL_row["nSports"] = nSports
    def set_nPolice(self, nPolice):
        self.SQL_row["nPolice"] = nPolice
    def set_nOthers(self, nOthers):
        self.SQL_row["nOthers"] = nOthers

    def as_dict(self):
        return self.SQL_row