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
        self.pk_timestamp = str(datetime.datetime.now())             # Primary Key timestamp / id
        self.db_datetime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))           # Primary Key timestamp / id
        # self.db_datetime = self.pk_timestamp.strftime('%Y-%m-%d %H:%M:%S')   # Momento de la Captura / captureDatetime

        print("Requesting...")
        self.requester.go_fetch()
        
        print("Scrapping...")
        self.scrapper.scraps.set_id(self.pk_timestamp)
        self.scrapper.scraps.set_captureDatetime(self.db_datetime)
        self.scrapper.go_scrape()
        


    # Consigna a las DBs lo scrappeado
    #   Dado que lo que se commitea a las DBs tiene que ser universalmente uniforme, este metodo no
    #   amerita el ser diferente para cada subclase: el ser unico implica una garantia de uniformidad
    def store(self):
        
        # #########################################################################################        
        # MongoDB Section
        # #########################################################################################        
        #  Esto se va a referir al scrape crudo tal cual lo obtuvo requester,
        #  self.requester.text
        self.mongo = MongoDB()
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
        self.mongo.upsertDict(self.scrapper.scraps.mongodb.as_dict(), 'TESTE', self.name)
        
        # print(self.scrapper.scraps.mongodb.as_dict())

        
        # import pprint
        # # #########################################################################################
        # # SQL Section
        # # #########################################################################################
        self.sql = SQLServer()        
        
        dd = self.scrapper.scraps.sql.as_dict()        
        dl = {k : [v] for (k, v) in dd.items()}
        df = pd.DataFrame(dl)
        self.sql.insert(df, "test_scrap3")      # TODO: En esta instancia, pandas's dataframe is overkill & overhead
        
        # print(df)
        
        # df = pd.DataFrame({'ID'                         : list( (self.name + '_' + str(self.pk_timestamp), ) ),
        #                    'MOMENTO_CAPTURA'            : list( (str(self.db_datetime), ) ),
        #                    'SITIO'                      : list( (self.name, ) ),
        #                                                 # tener en cuenta que self.scrapper.scraps 
        #                                                 # no existe hasta correr
        #                    'TITULO_PRINCIPAL'           : list( (self.scrapper.scraps['titulo_h1'], ) ),
        #                    'CATEGORIA_TITULO_PRINCIPAL' : list( (self.scrapper.scraps['titulo_href'].split('/')[1], ) ) })
        # 
        
        pass