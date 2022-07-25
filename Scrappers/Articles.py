# Articles.py -- a part of Scrappers
# this file should only be visible to Scrappers's files (e.g.: Scrapper.py & <target>Scrapper.py)

# Defines two classes. An Article() class which is an abstraccion of the datastructure of an article
# plus some methods to set its fields and retrieve afterwards, MainArticle(Article), a subclass
# which is just a dummy shim only meant for semantic differentiation -- it's internally the same

class Article():
    def __init__(self, title = None, slug = None, category = None, lead = None):
        self.article = {
            "title" : title,
            "slug" : slug,
            "category" : category,
            "lead" : lead,

            # Datamodel's 2nd Iteration
            # TODO: Photo on hold
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
        }

    def set_title(self, title):
        self.article["title"] = title

    def set_slug(self, slug):
        self.article["slug"] = slug

    def set_href(self, href):           # Alias to make clear that href & slug are synonyms
        self.article["slug"] = href

    def set_category(self, category):
        self.article["category"] = category

    def set_lead(self, lead):
        self.article["lead"] = lead

    # TODO: photo position seems like a hard inference... a placeholder for now
    # def set_photo_position(self, absolute, relative):    
    #     self.article["photo"]["abs"] = None
    #     self.article["photo"]["rel"] = None

    # TODO: photo size seems NOT that hard an inference... but still... a placeholder for now
    # def set_photo_size(self, absolute, relative):
    #     self.article["photo"]["abs"] = None
    #     self.article["photo"]["rel"] = None

    def category_as_SQL_key(self):
        if self.article["category"].lower() == "economia":
            return "nEconomics"
        elif self.article["category"].lower() == "politica":
            return "nPolitics"
        elif self.article["category"].lower() == "sociedad":
            return "nSociety"
        elif self.article["category"].lower() == "deporte":
            return "nSports"
        elif self.article["category"].lower() == "police":
            return "nPolice"
        else:
            return "nOthers"
    
    def title(self):
        return self.article["title"]

    def slug(self):
        return self.article["slug"]

    def href(self):
        return self.article["slug"]
    
    def category(self):
        return self.article["category"]

    def as_dict(self):
        return self.article

class MainArticle(Article):     # mainArticle is just an article. Same structure ... for now?
    pass