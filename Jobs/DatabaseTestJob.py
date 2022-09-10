# DatabaseTestJob.py -- Testing over the database
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@
# TODO: Keep in mind this file has been altered... and I don't even know where the fuck!!! :@

from pprint import pprint
import logging

from Jobs.Job import Job
from db_connectors.MongoDB.MongoDB import MongoDB

# from Requesters.TNRequester import TNRequester as Requester
# from Scrappers.TNScrapper import TNScrapper as Scrapper

class DatabaseTestJob(Job):
    def __init__(self, url = "https://tn.com.ar", headers = None, params = None, dbg = False):
        self.job_name = "DatabaseTest"
        
        try:    # connection
            self.mongo = MongoDB()
        except Exception as e:
            print("Failed to connect to MongoDB", e)
            logging.error("Failed to connect to MongoDB DataBase", exc_info = e, stack_info = True)
            raise   # propagate exception upwards
    def launch(self):
        try:    # instantiate a cursor
            self.dbcursor = self.mongo.read_all_as_cursor("TESTE", "SCRPPRJ_TN_rawdata")
        except Exception as e: # ... something goes wrong, in that case...
            print("Failed to get a cursor", e)  
            logging.error("Failed to get a cursor", exc_info = e, stack_info = True)

    def store(self, dummy):
        print('Dummy parameter ... controls if commit is done to file', dummy)
        with open('.test/mongodb_dump_file.txt', 'w') as f:
                for doc in self.dbcursor:
                    pprint(doc, stream = f)

