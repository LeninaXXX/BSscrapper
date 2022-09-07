# TODO: Re do

from db_connectors.Database import Database

from pymongo import MongoClient

import pandas as pd

import logging

class MongoDB(Database):
    def __init__(self):
        self.client = MongoClient('mongodb://administrador:p4s$w0Rd@172.16.7.19:27017')

    def upsertDF(self, df: pd.DataFrame, base, collection):
        db = self.client[base]
        # collection
        collection = db[collection]

        # Recorrer las filas del dataframe y guardar en la base de datos
        lista = {}
        for i,r in df.iterrows():
            for key in df.keys():
                lista[key] = r[key]
            id = lista.pop('id')
            collection.update_one({"_id" : id}, {"$set": lista}, upsert=True)

    def upsertDict(self, data: dict, base, collection):
        aDict = dict(data)
        
        # 
        db = self.client[base]
        collection = db[collection]
        
        try:
            id = aDict.pop('id')
            # Upsert
            collection.update_one(
                {"_id" : id},
                {"$set" : aDict},
                upsert=True
            )
        except Exception as e:
            logging.error('Failed to upload a dict')
            logging.error(aDict)

    def read_all_as_cursor(self, database, collection):
        "Returns a cursor over an entire collection"
        db = self.client[database]
        coll = db[collection]

        try:
            cursor = coll.find({})  # empty document should return *everything* (an interator over everything anyway...)
        except Exception as e:
            logging.error("Something went wrong when querying MongoDB", exc_info = e, stack_info = True)
            raise   # propagate upwards in the calling hierarchy
        else:       # XXX: Is this the proper way to handle it?
            return cursor

