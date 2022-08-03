
from Scrappers.Articles import Article
from Scrappers.Articles import MainArticle

class ScrapsMongoDB():
    def __init__(self, job_name = None, url = None, primary_key = None, capture_datetime = None, dbg = False):
        # DataModel Version Information
        self.datamodel_version = 1
        self.datamodel_revision = 0
        self.datamodel_iteration = "%s.%02s" % (str(self.datamodel_version), str(self.datamodel_revision))

        self.job_name = job_name
        self.url = url
        self.primary_key = primary_key
        self.capture_datetime = capture_datetime
        self.dbg = dbg

        # MongoDB DataModel - Datamodel 2nd Iteration        
        # Raw Data MongoDB Document Model
        self.MongoDB_raw_doc = {            
            "id" : self.primary_key,
            "datamodel_version" : self.datamodel_iteration,
            "jobName" : self.job_name,
            "captureDatetime" : self.capture_datetime,
            "url" : self.url,
            
            "rawData" : {
                "request_text" : None,
                "request_reason" : None,
                "request_status_code" : None,
                "request_apparent_encoding" : None
            }
        }
        # Cleaned MongoDB Document Model
        self.MongoDB_clean_doc = {
            "id" : self.primary_key,
            "datamodel_version" : self.datamodel_iteration,
            "jobName" : self.job_name,
            "captureDatetime" : self.capture_datetime,
            "url" : self.url,

            "annotations" : {
                "main_article" : {
                    "title" : None,
                    "slug" : None,
                    "category" : None,
                    "lead" : None,
                    # Datamodel's 2nd Iteration
                    # XXX: Photo on hold
                    # "photo" : {
                    #     "position" : {
                    #         "abs" : None,
                    #         "rel" : None
                    #     },
                    #     "size" : {
                    #         "abs" : None,
                    #         "rel" : None
                    #     }
                    # }                    
                },
                "articles" : []
            }
        }
        if self.dbg:     # if called in debug mode, tag database commit
            self.set_debug_flag()

    def set_debug_flag(self):
        self.MongoDB_raw_doc["DBG_FLAG"] = True
        self.MongoDB_clean_doc["DBG_FLAG"] = True

    def set_primary_key(self, primary_key):
        self.MongoDB_raw_doc["id"] = primary_key
        self.MongoDB_clean_doc["id"] = primary_key

    def set_capture_datetime(self, capture_datetime):
        self.MongoDB_raw_doc["captureDatetime"] = capture_datetime
        self.MongoDB_clean_doc["captureDatetime"] = capture_datetime

    def set_job_name(self, job_name):
        self.MongoDB_raw_doc["jobName"] = job_name
        self.MongoDB_clean_doc["jobName"] = job_name

    def set_url(self, url):
        self.MongoDB_raw_doc["url"] = url
        self.MongoDB_clean_doc["url"] = url

    def set_rawdata(self, ret, pruned_text):
        self.MongoDB_raw_doc["rawData"]["request_text"] = pruned_text
        self.MongoDB_raw_doc["rawData"]["request_reason"] = ret.reason
        self.MongoDB_raw_doc["rawData"]["request_status_code"] = ret.status_code
        self.MongoDB_raw_doc["rawData"]["request_apparent_encoding"] = ret.apparent_encoding
    
    def add_main_article(self, main_article: MainArticle):
        self.MongoDB_clean_doc["annotations"]["main_article"] = main_article.as_dict()

    def add_article(self, article: Article):
        self.MongoDB_clean_doc["annotations"]["articles"].append(article.as_dict())

    def append_articles(self, articles: list[Article]):
        for a in articles:
            self.add_article(a)

    # Datamodel's 2nd Iteration
    def add_annotation(self, ak, av):   # XXX : add an annotation
        self.MongoDB_clean_doc["annotations"][ak] = av

    # Datamodel's 2nd Iteration
    def add_annotation_dict(self, d):   # XXX : add multiple annotations given a dict
        for k in d:
            self.add_annotation(k, d[k])
            # self.MongoDB_clean_doc["annotations"][k] = d[k]

    def raw_as_dict(self):
        return self.MongoDB_raw_doc
    
    def clean_as_dict(self):
        return self.MongoDB_clean_doc
