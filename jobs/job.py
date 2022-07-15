# Job.py -- clase general

import pandas as pd
import datetime
import time

from Requesters.Requester import Requester
from Scrappers.Scrapper import Scrapper

from db_connectors.MongoDB.MongoDB import MongoDB
from db_connectors.SQLServer.SQLServer import SQLServer

class Job():
    # launch'ear el trabajo de requesting + scrapping: es competecia de este metodo
    #   operar requester y al scrapper y lidiar con las sutilezas de esa tarea
    def launch(self):
        # 'pk_timestamp' & 'db_datetime', computed at job launch time
        self.pk_timestamp = datetime.datetime.now()             # Primary Key timestamp / id
        self.db_datetime = time.strftime('%Y-%m-%d %H:%M:%S')   # Momento de la Captura / captureDatetime

        print("Requesting...")
        self.requester = Requester(self.url, headers = self.headers, params = self.params)
        self.requester.go_fetch()
        
        print("Scrapping...")
        self.scrapper = Scrapper(self.requester.payload_text(),     # TODO: to change to whole requests ret
                                 self.pk_timestamp, 
                                 self.db_datetime, 
                                 self.name, 
                                 self.url
                                )
        self.scrapper.go_scrape()

    # Consigna a las DBs lo scrappeado
    #   Dado que lo que se commitea a las DBs tiene que ser universalmente uniforme, este metodo no
    #   amerita el ser diferente para cada subclase: el ser unico implica una garantia de uniformidad
    def store(self):
        pass
        # #########################################################################################        
        # MongoDB Section
        # #########################################################################################        
        #  Esto se va a referir al scrape crudo tal cual lo obtuvo requester,
        #  self.requester.text
        # self.mongo = MongoDB()
        # mongo_pload = {}
        # 
        # # string'izar el timestamp como id unico en MongoDB
        # mongo_pload['id'] = self.name + '_' + str(self.db_datetime)    # TODO: Exception management
        # 
        # # se refiera al campo 'pload' del objeto job.requester de manera directa para
        # # construir el diccioario que va a upsert'ear en MongoDB. *ESTO ES MALA PRACTICA*
        # # TODO: Implementar interfaz que abstraiga ese acceso via metodos. DONE! 
        # mongo_pload['rawData'] = {}
        # mongo_pload['rawData']['requests_text'] = self.requester.pload.text
        # mongo_pload['rawData']['requests_reason'] = self.requester.pload.reason
        # mongo_pload['rawData']['requests_status_code'] = self.requester.pload.status_code
        # mongo_pload['rawData']['requests_apparent_encoding'] = self.requester.pload.apparent_encoding
        # 
        # mongo_pload['annotations'] = {}
        # 
        # self.mongo.upsertDict(mongo_pload, 'TESTE', self.name)
        # 
        # # #########################################################################################
        # # SQL Section
        # # #########################################################################################
        # self.sql = SQLServer()
        # df = pd.DataFrame({'ID'                         : list( (self.name + '_' + str(self.pk_timestamp), ) ),
        #                    'MOMENTO_CAPTURA'            : list( (str(self.db_datetime), ) ),
        #                    'SITIO'                      : list( (self.name, ) ),
        #                                                 # tener en cuenta que self.scrapper.scraps 
        #                                                 # no existe hasta correr
        #                    'TITULO_PRINCIPAL'           : list( (self.scrapper.scraps['titulo_h1'], ) ),
        #                    'CATEGORIA_TITULO_PRINCIPAL' : list( (self.scrapper.scraps['titulo_href'].split('/')[1], ) ) })
        # 
        # self.sql.insert(df, "test_scrap2")      # TODO: En esta instancia, pandas's dataframe is overkill & overhead
