# Scrapper.py -- general superclass

# this module should only be visible to Job.py

class Scrapper():
    def __init__(self, name, payload, primary_key = None, capture_datetime = None):
        
        self.scraps = Scraps(name = name,
							 primary_key = primary_key, 		# at this point, primary_key nor capture_datetime are set.
							 capture_date = capture_datetime)	# at this point, primary_key nor capture_datetime are set.
																# it's done at job.launch() time

	def set_primary_key(primary_key):
		self.scraps.set_id(primary_key)
		
	def set_capture_datetime(capture_datetime):
		self.scraps.set_capture_datetime(capture_datetime)
		
class Article():
    def __init__(self, title = None, slug = None, category = None, lead = None):
        self.article = {
            "title" : title,
            "slug" : slug,
            "category" : category,
            "lead" : lead,
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
        }

    def set_title(self, title):
        self.article["title"] = title

    def set_slug(self, slug):
        self.article["slug"] = slug

    def set_category(self, category):
        self.article["category"] = category

    def set_lead(self, lead):
        self.article["lead"] = lead

    # TODO: photo position seems like a hard inference... a placeholder for now
    def set_photo_position(self, absolute, relative):    
        self.article["photo"]["abs"] = None
        self.article["photo"]["rel"] = None

    # TODO: photo size seems not that hard an inference... but still... a placeholder for now
    def set_photo_size(self, absolute, relative):
        self.article["photo"]["abs"] = None
        self.article["photo"]["rel"] = None

    def category_as_SQL_key(self):
        if self.article["category"] == "Economics":
            return "nEconomics"
        elif self.article["category"] == "Politics":
            return "nPolitics"
        elif self.article["category"] == "Society":
            return "nSociety"
        elif self.article["category"] == "Sports":
            return "nSports"
        elif self.article["category"] == "Police":
            return "nPolice"
        else:
            return "nOthers"
    
    def title(self):
        return self.article["title"]

    def href(self):
        return self.article["slug"]
    
    def category(self):
        return self.article["category"]

    def as_dict(self):
        return self.article

class MainArticle(Article):     # mainArticle is just an article. Same structure ... for now?
    pass

class Scraps():    
    def __init__(self, job_name = None, primary_key = None, capture_datetime = None):
        # init SQL scraps
        self.sql = ScrapsSQL(job_name = job_name, 
							 primary_key = primary_key, 
							 capture_datetime = capture_datetime)
        # init MongoDB scraps
        self.mongodb = ScrapsMongoDB(job_name = job_name, 
									 primary_key = primary_key, 
									 capture_datetime = capture_datetime)

    def set_primary_key(self, primary_key):
        self.sql.set_primary_key(primary_key)
        self.mongodb.set_primary_key(primary_key)
    def set_capture_datetime(self, capture_datetime):
        self.sql.set_capture_datetime(capture_datetime)
        self.mongodb.set_capture_datetime(capture_datetime)
        
    def set_name(self, name):
        self.sql.set_name(name)
        self.mongodb.set_name(name)
    def set_url(self, url):
        self.sql.set_url(url)        
        self.mongodb.set_url(url)        

    def add_main_article(self, main_article: MainArticle):
        self.sql.set_mainArticleTitle = main_article.title()
        self.sql.set_mainArticleHref = main_article.href()
        self.sql.set_mainArticleCategory = main_article.category()
        self.mongodb.add_main_article(main_article)
    
    def add_article(self, article: Article):
        
        self.sql.SQL_row["nArticles"] += 1
        self.sql.SQL_row[article.category_as_SQL_key()] += 1
        self.mongodb.add_article(article)
    
    def append_articles(self, articles: list[Article]):
        for a in articles:
            self.sql.SQL_row[a.category_as_SQL_key()] += 1
        self.mongodb.append_articles(articles)        

class ScrapsSQL():
    def __init__(self, job_name = None, primary_key = None, capture_datetime = None):
        # SQL DataModel
        self.SQL_row = {
            "id" : primary_key,						# PRIMARY KEY : name + timestamp @ job launch time
            "name" : job_name,                      # Name of the target (e.g.: La_Nacion)
            "captureDatetime" : capture_datetime,   # datetime @ job launch time
            "url" : None,                           # ACTUAL url being scrapped 
            
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
        }

    def set_primary_key(self, primary_key):
        self.SQL_row["id"] = primary_key
    def set_capture_datetime(self, capture_datetime):
        self.SQL_row["captureDatetime"] = capture_datetime
        
    def set_name(self, name):
        self.SQL_row["name"] = name
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

class ScrapsMongoDB():
    def __init__(self, job_name = None, primary_key = None, capture_datetime = None):
        # MongoDB DataModel
        self.MongoDB_doc = {
            "id" : primary_key,
            "name" : job_name,
            "captureDateTime" : capture_datetime,
            "url" : None,
            
            "rawData" : {
                "request_text" : None,
                "request_reason" : None,
                "request_status_code" : None,
                "request_apparent_encoding" : None
            },
            
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
        self.MongoDB_doc["id"] = primary_key

    def set_capture_datetime(self, capture_datetime):
        self.MongoDB_doc["captureDatetime"] = capture_datetime

    def set_name(self, name):
        self.MongoDB_doc["name"] = name

    def set_url(self, url):
        self.MongoDB_doc["url"] = url

    def set_rawData(self, ret):
        self.MongoDB_doc["rawData"]["request_text"] = ret.text
        self.MongoDB_doc["rawData"]["request_reason"] = ret.reason
        self.MongoDB_doc["rawData"]["request_status_code"] = ret.status_code
        self.MongoDB_doc["rawData"]["request_apparent_encoding"] = ret.apparent_encoding
    
    def add_article(self, article: Article):
        self.MongoDB_doc["annotations"]["articles"].append(article.as_dict())

    def append_articles(self, articles: list[Article]):
        for a in articles:
            self.add_article(a)

    def add_main_article(self, main_article: MainArticle):
        self.MongoDB_doc["annotations"]["main_article"] = main_article.as_dict()

    def as_dict(self):
        return self.MongoDB_doc
