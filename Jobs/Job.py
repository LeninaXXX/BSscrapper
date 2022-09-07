# Job.py -- general superclass

import pandas as pd
import datetime
import time
import logging
import traceback

from Requesters.Requester import Requester
from Scrappers.Scrapper import Scrapper

from db_connectors.MongoDB.MongoDB import MongoDB
from db_connectors.SQLServer.SQLServer import SQLServer

class Job():    
    def launch(self):
		# Generate PRIMARY KEY & set capture_datetime at THIS moment
        self.primary_key = self.job_name + '_' + str(datetime.datetime.now())
        self.capture_datetime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.scrapper.set_primary_key(self.primary_key)             
        self.scrapper.set_capture_datetime(self.capture_datetime)       
        
        logging.info("Requesting... " + self.job_name)
        print("Requesting...", self.job_name)
        try:
            self.requester.go_fetch()
        except Exception as e:
            print("Error while requesting\n", e)
            logging.exception("Error while requesting", exc_info = e)
        
        logging.info("Scrapping... " + self.job_name)
        print("Scrapping...", self.job_name)
        try:
            self.scrapper.go_scrape(self.requester.payload())   # XXX : I don't like this explicit passing of the payload
        except Exception as e:
            print("Error while scrapping\n", e)
            logging.exception("Error while scrapping", exc_info = e)

    def store(self, file_commit = False):
        # if in normal operation, commit to database
        if not file_commit:
            # CONNECT TO MONGODB DATABASE
            try:    # guard for connection exceptions
                self.mongo_connection = MongoDB()
            except Exception as e:
                print("Failed to connect to MongoDB\n", e)
                logging.exception("Failed to connect to MongoDB DataBase", exc_info = e)
                # TODO: This should preclude further execution of the job, and should
                #   raise a user-defined exception tailored to manage such condition
                # Definition of exception exposing more detailed information pending
            
            # COMMIT TO MONGODB DATABASE
            try:    # guard for db commit exception
                self.mongo_connection.upsertDict(self.scrapper.get_MongoDB_raw_scraps_as_dict(), 'TESTE', 'SCRPPRJ_' + self.job_name + '_rawdata')
            except Exception as e:
                print("Failed to commit to Mongo DB\n", e)
                logging.exception("Failed to commit to Mongo DB", exc_info = e)
                # TODO: This should preclude further execution of the job, and should
                #   raise a user-defined exception tailored to manage such condition
                # Definition of exception exposing more detailed information pending

        # if in debug mode, dump to file for inspection
        else:
            import json     # import json module lazily
            try:
                with open('.test/output/' + self.job_name + '_MongoDB_dbg_dump.txt', 'a') as f:
                    print(json.dumps(self.scrapper.get_MongoDB_raw_scraps_as_dict(), indent=4), file = f)
            except Exception as e:
                print("Something failed when writing to file\n", e)
                logging.exception("Something failed when writing to file", exc_info = e)

        # FIXME: Dumping into a file and flagging as DEBUG should be two orthogonal features

        