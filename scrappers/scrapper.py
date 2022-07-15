# Scrappere.py -- clase general

# este modulo deberia ser solo visible a target

import bs4 as bs
import html5lib 
import datetime

class Scrapper():
    def __init__(self, text, pk_timestamp, db_timestamp, name, url):
        self.pk_timestamp = pk_timestamp
        self.db_timestamp = db_timestamp
        self.scraps = Scraps(id = pk_timestamp, captureDatetime = db_timestamp, name = name, url = url)
        
        self.soup = bs.BeautifulSoup(text, "html5lib")
        # TODO: BeautifulSoup admite varios parsers html/xml
        # Este hardwireo es medio asqueroso y deberia admitir generalizacion 
        # que a su vez admita mas versatilidad al ser usado desde 'Job'
       
        # self.Scraps = None    # Where the scrapped stuff is gonna be 
                                # tucked away in *SOME* representation
                                # still to be well-defined
        # esto no va a estar definido hasta tanto no se tire un go_scrape()

    # Este metodo va a proveer accesso a la representacion piola del scrape
    # (por representacion piola se entiende una que 'calque' el data model de la database)
    # ... no veo razon para que la representacion interna del scrap 
    #     en la clase/instancia no sea ya la 'representacion piola'
    # def payload(self):
    #     try:                    # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
    #         return self.scraps  # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
    #     except:                 # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
    #         self.go_scrape()    # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
    #         return self.scraps  # BOILERPLATE!: Which exception? NameError? AttributeError? ... both?
    # 
    # # esto esta mostly con fines de debugging, para ver si el scrapper 
    # # esta (valga la redundancia...) scrappeando lo que yo quiero
    # def payload_as_text(self):
    #     try:
    #         return self.scraps.__repr__()   # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
    #     except:                             # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
    #         self.go_scrape()                # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
    #         return self.scraps.__repr__()   # BOILERPLATE!: which exception? Should call self.payload() and then textify that?
    #     # TODO: Aun para fines de debugging, JSON es la que va...

# #############################################################################
# Article, modeled a class with an interface
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
    def set_photo_position(self, abs, rel):    
        self.article["photo"]["abs"] = None
        self.article["photo"]["rel"] = None

    # TODO: photo size seems not that hard an inference... but still... a placeholder for now
    def set_photo_size(self, abs, rel):
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

# #############################################################################
# MainArticle, a subclass of Article
class MainArticle(Article):     # just for consistency's sake -- mainArticle is an article
    pass

# ################
# Scraps container
# #################################################################################################
# va a hacer las veces de 'bundle' de todo lo que 'job.store()' tenga que commitear a las databases
class Scraps():    
    def __init__(self, id = None, captureDatetime = None, name = None, url = None):
        self.sql = ScrapsSQL(id, captureDatetime, name, url)
        self.mongodb = ScrapsMongoDB(id, captureDatetime, name, url)

    def set_id(self, id):
        self.sql.set_id(id)
        self.mongodb.set_id(id)
    def set_captureDatetime(self, captureDatetime):
        self.sql.set_captureDatetime(captureDatetime)
        self.mongodb.set_captureDatetime(captureDatetime)
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

# ######################################
# Scraps container to be inserted in SQL
# ######################################
# wrappea un dict + un conjunto de metodos con el que abstraer el accederlo
class ScrapsSQL():
    def __init__(self, id = None, captureDatetime = None, name = None, url = None):
        # SQL DataModel
        self.SQL_row = {
            "id" : id,                              # PRIMARY KEY : name + timestamp @ job launch time
            "captureDatetime" : captureDatetime,    # datetime @ job launch time
            "name" : name,                          # Name of the target (e.g.: La_Nacion)
            "url" : url,                            # ACTUAL url being scrapped 
            
            "mainArticleTitle" : None,      # 
            "mainArticleHref" : None,       # relative url of main article
            "mainArticleCategory" : None,   # category as infered (e.g.: from slug)
            
            "nArticles" : 0,                # number of articles
            "nEconomics" : 0,               # number of articles in the category of 'economics'
            "nPolitics" : 0,                # ... politics
            "nSociety" : 0,                 # ... society
            "nSports" : 0,                  # ... sports
            "nPolice" : 0,                  # ... police
            "nOthers" : 0                   # number on a category not known in advance
        }

    def set_id(self, id):
        self.SQL_row["id"] = id
    def set_captureDatetime(self, captureDatetime):
        self.SQL_row["captureDatetime"] = captureDatetime
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

# ##########################################
# Scraps container to be inserted in MongoDB
# ##########################################
class ScrapsMongoDB():
    def __init__(self, id = None, captureDatetime = None, name = None, url = None):
        self.MongoDB_doc = {
            "id" : id,
            "captureDateTime" : captureDatetime,
            "name" : name,
            "url" : url,
            
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
                "articles" : []     # ... a list of dict, each one w/same structure as main_article
            }
        }

    def set_id(self, id):
        self.MongoDB_doc["id"] = id

    def set_captureDatetime(self, captureDatetime):
        self.MongoDB_doc["captureDatetime"] = captureDatetime

    def set_name(self, name):
        self.MongoDB_doc["name"] = name

    def set_url(self, url):
        self.MongoDB_doc["url"] = url

    def set_rawData(self, ret):     # req is supposed to be a requests returned object
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
