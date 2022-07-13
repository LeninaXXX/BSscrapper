# job.py -- clase general

import sqlite3
import pandas as pd

from requesters.requester import requester
from scrappers.scrapper import scrapper

from db_connectors.MongoDB.MongoDB import MongoDB
from db_connectors.SQLServer.SQLServer import SQLServer

class job():
    # Consigna a las DBs lo scrappeado
    #   Dado que lo que se commitea a las DBs tiene que ser universalmente uniforme, este metodo no
    #   no parece ameritar bajo ningun punto de vista el ser diferente para cada subclase: el ser
    #   unico implica una garantia de uniformidad
    def store(self):
        # #########################################################################################        
        # MongoDB Section
        # #########################################################################################        
        #  Esto se va a referir al scrape crudo tal cual lo obtuvo requester,
        #  self.requester.text
        self.mongo = MongoDB()
        mongo_pload = {}
        
        # string'izar el timestamp como id unico en MongoDB
        mongo_pload['id'] = self.name + '_' + str(self.sql_datetime)    # TODO: Exception management
        
        # se refiera al campo 'pload' del objeto job.requester de manera directa para
        # construir el diccioario que va a upsert'ear en MongoDB. *ESTO ES MALA PRACTICA*
        # TODO: Implementar interfaz que abstraiga ese acceso via metodos.
        mongo_pload['payload'] = {}
        mongo_pload['payload']['requests_text'] = self.requester.pload.text
        mongo_pload['payload']['requests_reason'] = self.requester.pload.reason
        mongo_pload['payload']['requests_status_code'] = self.requester.pload.status_code
        mongo_pload['payload']['requests_apparent_encoding'] = self.requester.pload.apparent_encoding

        mongo_pload['annotations'] = {}
        # "wrapping" del "regalito"

        # mongo_pload['annotations']['nota1']
        # 
        # Notas que aparecen 
        #   - nota principal
        #   - titulos
        #   - y sus categorias
        # Ubicacion y tamaño de foto principal asociada al titulo principal
        #
        self.mongo.upsertDict(mongo_pload, 'TESTE', self.name)

        # #########################################################################################
        # SQL Section
        # #########################################################################################
        self.sql = SQLServer()

        # id = []; id.append(self.name + str(self.datetime))
        # momento_captura = []; momento_captura.append(str(self.datetime))
        # sitio = []; sitio.append("LaNacion")
        # titulo_principal = []; titulo_principal.append("LaNacion")
        # categoria_titulo_principal = []; categoria_titulo_principal.append('Politica')
        df = pd.DataFrame({'ID'                         : list( (self.name + '_' + str(self.uid_timestamp), ) ),
                          #'MOMENTO_CAPTURA'            : list( (str(self.sql_datetime), ) ),
                           'MOMENTO_CAPTURA'            : list( (str(self.sql_datetime), ) ),
                           'SITIO'                      : list( (self.name, ) ),
                                                        # tener en cuenta que self.scrapper.scraps 
                                                        # no existe hasta correr
                           'TITULO_PRINCIPAL'           : list( (self.scrapper.scraps['titulo_h1'], ) ),
                           'CATEGORIA_TITULO_PRINCIPAL' : list( (self.scrapper.scraps['titulo_href'].split('/')[1], ) ) })
        # self.sql.upsert(df, "test_scrap") 

        # informacion estadistica
        #  titulo principal
        #  categoria titulo principal
        #  Cuantas notas
        #  Cuantas notas de cada categoria (numericamente)

        self.sql.insert(df, "test_scrap2")




