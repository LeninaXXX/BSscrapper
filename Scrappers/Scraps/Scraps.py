from Scrappers.Articles import Article
from Scrappers.Articles import MainArticle
from Scrappers.Scraps.ScrapsSQL import ScrapsSQL
from Scrappers.Scraps.ScrapsMongoDB import ScrapsMongoDB

class Scraps():
    def __init__(self, job_name = None, url = None, primary_key = None, capture_datetime = None, dbg = False):
        # init MongoDB scraps
        self.scraps_MongoDB = ScrapsMongoDB(job_name = job_name, 
									        url = url,
                                            primary_key = primary_key, 
									        capture_datetime = capture_datetime,
                                            dbg = dbg)

        # init SQL scraps
        self.scraps_SQL = ScrapsSQL(job_name = job_name, 
                                    url = url, 
		                            primary_key = primary_key,
		                            capture_datetime = capture_datetime,
                                    dbg = dbg)

    def set_debug_flag(self ):               # Instead of manually flipping it on, it's propagated from constructor to
        self.scraps_MongoDB.set_debug_flag() # Left it as an utility function just in case. Not actually used
        # self.scraps_SQL.set_debug_flag()     # constructor scraps constructors inherit the concern of tagging db commits.
                                                    
    def set_primary_key(self, primary_key):
        self.scraps_MongoDB.set_primary_key(primary_key)
        # self.scraps_SQL.set_primary_key(primary_key)
    def set_capture_datetime(self, capture_datetime):
        self.scraps_MongoDB.set_capture_datetime(capture_datetime)
        # self.scraps_SQL.set_capture_datetime(capture_datetime)
    def set_name(self, name):
        self.scraps_MongoDB.set_job_name(name)
        # self.scraps_SQL.set_name(name)
    def set_url(self, url):
        self.scraps_MongoDB.set_url(url)
        # self.scraps_SQL.set_url(url)        

    def set_rawdata(self, ret, pruned_text):
        self.scraps_MongoDB.set_rawdata(ret, pruned_text)

    def add_main_article(self, main_article: MainArticle):
        self.scraps_MongoDB.add_main_article(main_article)
        # MainArticle is also an Article
        # self.scraps_SQL.SQL_row["nArticles"] += 1   # TODO: Abstract access to internal rep
        # self.scraps_SQL.SQL_row[main_article.category_as_SQL_key()] += 1 # TODO: Abstract access to internal rep
        # self.scraps_SQL.set_mainArticleTitle(main_article.title())
        # self.scraps_SQL.set_mainArticleHref(main_article.href())
        # self.scraps_SQL.set_mainArticleCategory(main_article.category())
    
    def add_article(self, article: Article):        
        self.scraps_MongoDB.add_article(article)
        # self.scraps_SQL.SQL_row["nArticles"] += 1   # TODO: Abstract access to internal rep
        # self.scraps_SQL.SQL_row[article.category_as_SQL_key()] += 1 # TODO: Abstract access to internal rep
    
    def append_articles(self, articles: list[Article]):
        self.scraps_MongoDB.append_articles(articles)
        # for a in articles:
        #     self.scraps_SQL.SQL_row[a.category_as_SQL_key()] += 1
        #     self.scraps_SQL.SQL_row["nArticles"] += 1

    # Page's physical layout, metadata, and stuff not presented to the final consumer
    def doc_level0(self):
        return self.scraps_MongoDB.doc_level0()
    
    def doc_level0(self):
        return self.scraps_MongoDB.doc_level0()

    # These are just redirectors to the appropriate fuctions in ScrapsSQL
    def SQL_stash_row(self, row):
        return self.scraps_SQL.stash_row(row)

    # These are just redirectors to the appropriate fuctions in ScrapsSQL
    def SQL_stash_row_given_schema(self, row, schema):
        return self.scraps_SQL.stash_row_given_schema(row, schema)


    def SQL_as_lists_list(self):
        return self.scraps_SQL.as_lists_list()
    
    def SQL_dump_as_string(self):
        return self.scraps_SQL.dump_as_string()
