# Job.py -- general superclass

import pandas as pd
import datetime
import time
import logging

from Requesters.Requester import Requester
from Scrappers.Scrapper import Scrapper

from db_connectors.MongoDB.MongoDB import MongoDB
from db_connectors.SQLServer.SQLServer import SQLServer

class Job():    
    def launch(self):
		# Generate PRIMARY KEY & set capture_datetime at THIS moment
        self.primary_key = self.name + '_' + str(datetime.datetime.now())
        self.capture_datetime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        logging.info("Requesting... " + self.name)
        print("Requesting...", self.name)
        self.requester.go_fetch()
        
        logging.info("Scrapping... " + self.name)
        print("Scrapping...", self.name)
        self.scrapper.set_primary_key(self.primary_key)
        self.scrapper.set_capture_datetime(self.capture_datetime)       
        
        self.scrapper.go_scrape(self.requester.payload())

    def store(self):
        # from pprint import pprint   # XXX: DEBUGGING STUFF
        import json
        with open('.test/output/' + self.name + '_MongoDB_raw.txt', 'a') as f:
            # print("MongoDB RawData", file = f)
            # print("---------------", file = f)
            print(json.dumps(self.scrapper.get_MongoDB_raw_scraps_as_dict(), indent=4), file = f)
        
        self.mongo = MongoDB()
        self.mongo.upsertDict(self.scrapper.get_MongoDB_raw_scraps_as_dict(), 'TESTE', 'SCRPPRJ_' + self.name + '_rawdata')

"""
        with open('.test\output\MongoDB_cln.txt', 'w') as f:
            # print("\nMongoDB CleanData", file = f)
            # print("-----------------", file = f)
            print(json.dumps(self.scrapper.get_MongoDB_clean_scraps_as_dict(), indent=4), file = f)
        
        with open('.test\output\SQLScraps.txt', 'w') as f:
            # print("\nSQL Scraps", file = f)
            # print("----------", file = f)
            print(json.dumps(self.scrapper.get_SQL_scraps_as_dict(), indent=4), file = f)
"""

#        # MongoDB insertions
#        self.mongo = MongoDB()    
#        self.mongo.upsertDict(self.scrapper.get_MongoDB_raw_scraps_as_dict(), 'TESTE', self.name + '_rawdata')
#        self.mongo.upsertDict(self.scrapper.get_MongoDB_clean_scraps_as_dict(), 'TESTE', self.name + '_cleansed')
#        
#        # SQL insertions
#        # given the SQL connector at hand, which take pandas's DataFrames as input, this requires some massaging
#        self.sql = SQLServer()
#        df = pd.DataFrame({k : [v] for (k, v) in self.scrapper.get_SQL_scraps_as_dict().items()})
#        self.sql.insert(df, "test_scrap")   # TODO: En esta instancia, pandas's dataframe is overkill & overhead

        # self.sql = SQLServer()        
        #         dd = self.scrapper.scraps.sql.as_dict()        
        # dl = {k : [v] for (k, v) in dd.items()}
        # df = pd.DataFrame(dl)
        # self.sql.insert(df, "test_scrap3")      # TODO: En esta instancia, pandas's dataframe is overkill & overhead

