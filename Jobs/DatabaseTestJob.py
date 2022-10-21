# DatabaseTestJob.py -- Testing over the database

from pprint import pprint
import logging
import os

from Jobs.Job import Job
from db_connectors.MongoDB.MongoDB import MongoDB

class DatabaseTestJob(Job):
    def __init__(self, url = None, headers = None, params = None, dbg = False):
        self.job_name = "DatabaseTest"
        self.cursors_by_collection = {"SCRPPRJ_Ambito_Financiero_rawdata" : None, 
                                      "SCRPPRJ_Clarin_rawdata"            : None, 
                                      "SCRPPRJ_Infobae_rawdata"           : None, 
                                      "SCRPPRJ_La_Nacion_rawdata"         : None, 
                                      "SCRPPRJ_La100_rawdata"             : None, 
                                      "SCRPPRJ_Pagina_12_rawdata"         : None, 
                                      "SCRPPRJ_Radio_Mitre_rawdata"       : None, 
                                      "SCRPPRJ_TN_rawdata"                : None}
        try:    # connection
            self.mongo = MongoDB()
        except Exception as e:
            print("Failed to connect to MongoDB", e)
            logging.error("Failed to connect to MongoDB DataBase", exc_info = e, stack_info = True)
            raise   # propagate exception upwards

    def launch(self):
        """
        If everything goes according to plan, this procedure should have left a cursor ready
        to access each collection in the database. Each of those cursors is able to iterate
        over THE ENTIRE COLLECTION.
        """
        for collection in self.cursors_by_collection:
            try:
                self.cursors_by_collection[collection] = self.mongo.read_all_as_cursor("TESTE", collection)
            except Exception as e:
                print(f"Failed to get cursor for collection {collection}")
                print(f"Exception information", e)
                logging.error(f"Failed to get cursor for collection {collection}")
                logging.error(f"Exception information", exc_info=e)
                logging.error(f"Stacktrace information", stack_info = True)

    def store(self, dummy):
        print('Dummy parameter ... controls if commit is done to file:', dummy)
        for collection in self.cursors_by_collection:
            # os.makedirs(".test/" + collection, exist_ok = True)
            for doc in self.cursors_by_collection[collection]:
                print(collection, list(doc.keys()))
                print('\t_id', doc['_id'])
                print('\tcaptureDatetime', doc['captureDatetime'])
                print('\tjobName', doc['jobName'])
                print('\trawData', '####')
                print('\turl', doc['url'])
                break

#       with open('.test/mongodb_dump_file.txt', 'w') as f:
#               for doc in self.dbcursor:
#                   print(type(doc))
#                   pprint(doc, stream = f)

