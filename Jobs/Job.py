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
            logging.error("Error while requesting", exc_info = e)
        
        logging.info("Scrapping... " + self.job_name)
        print("Scrapping...", self.job_name)
        try:
            self.scrapper.go_scrape(self.requester.payload())   # XXX : I don't like this explicit passing of the payload
        except Exception as e:
            print("Error while scrapping\n", e)
            logging.error("Error while scrapping", exc_info = e)

    def store(self, file_commit = False):
        # if in normal operation, commit to database
        if not file_commit:
            # CONNECT TO MONGODB DATABASE
            # ###########################
            try:    # guard for connection exceptions
                self.mongo_connection = MongoDB()
            except Exception as e:
                print("Failed to connect to MongoDB\n", e)
                logging.error("Failed to connect to MongoDB DataBase", exc_info = e)
                # TODO: This should preclude further execution of the job, and should
                #   raise a user-defined exception tailored to manage such condition
                # Definition of exception exposing more detailed information pending
            
            # COMMIT TO MONGODB DATABASE
            # ##########################
            try:    # guard for db commit exception
                self.mongo_connection.upsertDict(self.scrapper.get_MongoDB_raw_scraps_as_dict(), 'TESTE', 'SCRPPRJ_' + self.job_name + '_rawdata')
                self.mongo_connection.upsertDict(self.scrapper.get_MongoDB_clean_scraps_as_dict(), 'TESTE', 'SCRPPRJ_' + self.job_name + '_cleandata')
            except Exception as e:
                print("Failed to commit to Mongo DB\n", e)
                logging.error("Failed to commit to Mongo DB", exc_info = e)
                # TODO: This should preclude further execution of the job, and should
                #   raise a user-defined exception tailored to manage such condition
                # Definition of exception exposing more detailed information pending

            # CONNECT TO SQL DATABASE
            # #######################
            try:    # guard for connection exceptions
                self.sql_connection = SQLServer()
            except Exception as e:    
                print("Failed to connect to SQL\n", e)
                logging.error("Failed to connect to SQL DataBase", exc_info = e)
            # COMMIT TO SQL DATABASE
            # ######################
            try:
                # FIXME: 02/11/2022 during InfobaeScrapper.py dev'ment
                # ... this is kludge is in order to deal with the fact that different jobs are using different tables
                self.sql_connection.insert_list_of_lists(self.job_sql_table,        # table pointed to by the job -- declared in <target>Job.py
                                                         self.scrapper.SQL_cols,    # 
                                                         self.scrapper.scraps.scraps_SQL.as_lists_list())               # This should work as it is
                
                # 02/11/2022 during InfobaeScrapper.py dev'ment
                # self.sql_connection.insert_list_of_lists('articles_scrap_v1', 
                #                                          self.scrapper.scraps.scraps_SQL.SQL_articles_scrap_v1_cols, 
                #                                          self.scrapper.scraps.scraps_SQL.as_lists_list())

            except Exception as e:                      # FIXME: Unmitigated disaster
                print("Failed to insert/commit to SQL\n", e)
                logging.error("Failed to insert/commit to SQL\n", exc_info = e)

        # if in debug mode, dump to file for inspection
        else:
            import json     # import json module lazily
            from pprint import pprint   # NOTE: Stopgap measure -- not able to dump to file using json module
            
            # MongoDB: Dump raw MongoDB scraps
            # ################################
            try:
                with open('.test/output/' + self.job_name + '_MongoDB_dbg_dump-rawdata.txt', 'w') as f:
                  # print(json.dumps(self.scrapper.get_MongoDB_raw_scraps_as_dict(), indent=4), file = f)
                    pprint(self.scrapper.get_MongoDB_raw_scraps_as_dict(), stream = f)
            except Exception as e:
                print("Something failed when writing MongoDB raw scraps to file\n", e)
                logging.error("Something failed when writing MongoDB raw scraps to file", exc_info = e)
            
            # MongoDB: Dump clean MongoDB scraps ... in different files
            # #########################################################
            try:
                with open('.test/output/' + self.job_name + '_MongoDB_dbg_dump-cleandata.txt', 'w') as f:
                  # print(json.dumps(self.scrapper.get_MongoDB_raw_scraps_as_dict(), indent=4), file = f)
                    pprint(self.scrapper.get_MongoDB_clean_scraps_as_dict() , stream = f)
            except Exception as e:
                print("Something failed when writing MongoDB cleandata to file\n", e)
                logging.error("Something failed when writing MongoDB cleandata to file", exc_info = e)

            # SQL: Dump SQL scraps ... in different files
            # ###########################################
            try:
                with open('.test/output/' + self.job_name + '_SQL_dbg_dump.txt', 'w') as f:
                  # print(json.dumps(self.scrapper.get_MongoDB_raw_scraps_as_dict(), indent=4), file = f)
                    pprint(self.scrapper.scraps.scraps_SQL.as_lists_list(), stream = f) 
                    # pprint(self.scrapper.scraps.scraps_SQL.as_lists_list(), stream = f) 
                    # FIXME: this should be accessed by an indirection on the scrapper
            except Exception as e:
                print("Something failed when writing SQL scraps to file\n", e)
                logging.error("Something failed when writing SQL scraps to file", exc_info = e)

        # FIXME: Dumping into a file and flagging as DEBUG should be two orthogonal features

        