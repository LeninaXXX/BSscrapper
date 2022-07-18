# Job.py -- general superclass

import pandas as pd
import datetime
import time

from Requesters.Requester import Requester
from Scrappers.Scrapper import Scrapper

from db_connectors.MongoDB.MongoDB import MongoDB
from db_connectors.SQLServer.SQLServer import SQLServer

class Job():    
    def launch(self):
		# Generate PRIMARY KEY & set capture_datetime at THIS moment
        self.primary_key = self.name + '_' + str(datetime.datetime.now())
        self.capture_datetime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        print("Requesting...")
        self.requester.go_fetch()
        
        print("Scrapping...")
        self.scrapper.set_primary_key(self.primary_key)
        self.scrapper.set_capture_datetime(self.capture_datetime)
        
        self.scrapper.go_scrape()

    def store(self):
		
        # self.mongo = MongoDB()        # 
        # self.mongo.upsertDict(self.scrapper.scraps.mongodb.as_dict(), 'TESTE', self.name)
        # 
        # self.sql = SQLServer()        
        #         dd = self.scrapper.scraps.sql.as_dict()        
        # dl = {k : [v] for (k, v) in dd.items()}
        # df = pd.DataFrame(dl)
        # self.sql.insert(df, "test_scrap3")      # TODO: En esta instancia, pandas's dataframe is overkill & overhead
		
