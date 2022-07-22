from Scrappers.Articles import Article
from Scrappers.Articles import MainArticle
from Scrappers.Scraps.ScrapsSQL import ScrapsSQL
from Scrappers.Scraps.ScrapsMongoDB import ScrapsMongoDB

class Scraps():
    def __init__(self, job_name = None, url = None, primary_key = None, capture_datetime = None):
        # init SQL scraps
        self.scraps_SQL = ScrapsSQL(job_name = job_name, 
                                    url = url, 
							        primary_key = primary_key, 
							        capture_datetime = capture_datetime)
        # init MongoDB scraps
        self.scraps_MongoDB = ScrapsMongoDB(job_name = job_name, 
									        url = url,
                                            primary_key = primary_key, 
									        capture_datetime = capture_datetime)

    def set_primary_key(self, primary_key):
        self.scraps_SQL.set_primary_key(primary_key)
        self.scraps_MongoDB.set_primary_key(primary_key)
    def set_capture_datetime(self, capture_datetime):
        self.scraps_SQL.set_capture_datetime(capture_datetime)
        self.scraps_MongoDB.set_capture_datetime(capture_datetime)
    def set_name(self, name):
        self.scraps_SQL.set_name(name)
        self.scraps_MongoDB.set_job_name(name)
    def set_url(self, url):
        self.scraps_SQL.set_url(url)        
        self.scraps_MongoDB.set_url(url)

    def set_rawdata(self, ret, pruned_text):
        self.scraps_MongoDB.set_rawdata(ret, pruned_text)

    def add_main_article(self, main_article: MainArticle):
        # MainArticle is also an Article
        self.scraps_SQL.SQL_row["nArticles"] += 1   # TODO: Abstract access to internal rep
        self.scraps_SQL.SQL_row[main_article.category_as_SQL_key()] += 1 # TODO: Abstract access to internal rep
        self.scraps_SQL.set_mainArticleTitle(main_article.title())
        self.scraps_SQL.set_mainArticleHref(main_article.href())
        self.scraps_SQL.set_mainArticleCategory(main_article.category())
        self.scraps_MongoDB.add_main_article(main_article)
    
    def add_article(self, article: Article):        
        self.scraps_SQL.SQL_row["nArticles"] += 1   # TODO: Abstract access to internal rep
        self.scraps_SQL.SQL_row[article.category_as_SQL_key()] += 1 # TODO: Abstract access to internal rep
        self.scraps_MongoDB.add_article(article)
    
    def append_articles(self, articles: list[Article]):
        for a in articles:
            self.scraps_SQL.SQL_row[a.category_as_SQL_key()] += 1
            self.scraps_SQL.SQL_row["nArticles"] += 1
        self.scraps_MongoDB.append_articles(articles)