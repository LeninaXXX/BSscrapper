
from Scrappers.Articles import Article
from Scrappers.Articles import MainArticle

class ScrapsMongoDB():
    def __init__(self, job_name = None, primary_key = None, capture_datetime = None):
        # MongoDB DataModel
        
        self.MongoDB_raw_doc = {            
            "id" : primary_key,
            "jobName" : job_name,
            "captureDatetime" : capture_datetime,
            "url" : None,
            
            "rawData" : {
                "request_text" : None,
                "request_reason" : None,
                "request_status_code" : None,
                "request_apparent_encoding" : None
            }
        }

        self.MongoDB_clean_doc = {
            "id" : primary_key,
            "jobName" : job_name,
            "captureDatetime" : capture_datetime,
            "url" : None,

            "annotations" : {
                "main_article" : {
                    "title" : None,
                    "slug" : None,
                    "category" : None,
                    "lead" : None,
                    "photo" : {
                        "position" : {
                            "abs" : None,
                            "rel" : None
                        },
                        "size" : {
                            "abs" : None,
                            "rel" : None
                        }
                    }
                },
                "articles" : []
            }
        }
        
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

    def set_rawdata(self, ret):
        self.MongoDB_raw_doc["rawData"]["request_text"] = ret.text
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

    def raw_as_dict(self):
        return self.MongoDB_raw_doc
    def clean_as_dict(self):
        return self.MongoDB_clean_doc
