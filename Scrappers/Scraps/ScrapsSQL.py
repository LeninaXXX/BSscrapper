import datetime
import logging
# from typing import OrderedDict
from collections import namedtuple


# This documents the columns of articles_scrap_v1 table.
SQL_articles_scrap_v1_schema = {'UKEY'              : 100,  # TODO: use this to build the row named tuple, and
                                'JOB'               : 50,   #   tune it to allow for data validation. For now,
                                'TITLE'             : 200,  #   it's only meant to allow for the checking of
                                'TITLE_WORD_COUNT'  : None, #   field lengths, but it should allow also for the
                                'AUTHOR'            : 50,   #   checking of int() type and date()s, maybe by
                                'SUMMARY'           : 500,  #   by storing a reference to a function.
                                'VOLANTA'           : 100,
                                'CATEGORY'          : 100,
                                'SLUG'              : 300,
                                'Origen'            : 50,
                                'FechaFiltro'       : None,
                                'FechaCreacion'     : None,
                                'FechaModificacion' : None
                               }

SQL_articles_scrap_v2_schema = {'UKEY'                    : 100,   # From InfobaeScrapper
                                'JOB'                     : 50,
                                'TITLE'                   : 200,
                                'TITLE_WORD_COUNT'        : None,
                                'ARTICLE'                 : 50,   # New field - Article number among articles
                                'CLUSTER'                 : None,   # New field - Cluster number to which this article belongs
                                'CLUSTER_INDEX'           : None,   # New field - Article number inside cluster
                                'CLUSTER_SIZE'            : None,   # New field - Size of the cluster to which this belongs
                                'CLUSTER_UNIQUE'          : None,   # New field - does this artice belong to a single cluster?
                                'AUTHOR'                  : 50,
                                'SUMMARY'                 : 500,
                                'VOLANTA'                 : 100,
                                'CATEGORY'                : 100,
                                'SUBCATEGORY'             : 100,   # New field - 
                                'SLUG'                    : 300,
                                'SLUG_INTERNAL'           : None,  # New field -
                                'Origen'                  : 50,
                                'FechaFiltro'             : None,
                                'FechaCreacion'           : None,
                                'FechaModificacion'       : None,
                               }

SQLArticlesScrapV2Row = namedtuple('SQLArticlesScrapV2Row',     # CREATE TABLE articles_scrap_v2 (
                                   [ 'UKEY',                    #   UKEY VARCHAR(100),
                                     'JOB',                     #   JOB VARCHAR(50),
                                     'TITLE',                   #   TITLE VARCHAR(200),
                                     'TITLE_WORD_COUNT',        #   TITLE_WORD_COUNT INT,
                                     'ARTICLE',                 #   ARTICLE INT,
                                     'CLUSTER',                 #   CLUSTER INT,       
                                     'CLUSTER_INDEX',           #   CLUSTER_INDEX INT,
                                     'CLUSTER_SIZE',            #   CLUSTER_SIZE INT,   
                                     'CLUSTER_UNIQUE',          #   CLUSTER_UNIQUE INT, 
                                     'AUTHOR',                  #   AUTHOR VARCHAR(50),
                                     'SUMMARY',                 #   SUMMARY VARCHAR(500),
                                     'VOLANTA',                 #   VOLANTA VARCHAR(100),
                                     'CATEGORY',                #   CATEGORY VARCHAR(100),
                                     'SUBCATEGORY',             #   SUBCATEGORY VARCHAR(100),
                                     'SLUG',                    #   SLUG VARCHAR(300),
                                     'SLUG_INTERNAL',           #   SLUG_INTERNAL INT,
                                     'Origen',                  #   Origen VARCHAR(50),         
                                     'FechaFiltro',             #   FechaFiltro DATE,    
                                     'FechaCreacion',           #   FechaCreacion DATE,  
                                     'FechaModificacion',       #   FechaModificacion DATE
                                   ],                           # )
                                   defaults = [None] * 20
                                  )

SQLArticlesScrapV1Row = namedtuple('SQLArticlesScrapV1Row',     # CREATE TABLE articles_scrap_v1 (
                                   [ 'UKEY',                    # 	UKEY VARCHAR(100),
                                     'JOB',                     # 	JOB VARCHAR(50),
                                     'TITLE',                   # 	TITLE VARCHAR(200),
                                     'TITLE_WORD_COUNT',        # 	TITLE_WORD_COUNT INT,
                                     'AUTHOR',                  # 	AUTHOR VARCHAR(50),
                                     'SUMMARY',                 # 	SUMMARY VARCHAR(500),
                                     'VOLANTA',                 # 	VOLANTA VARCHAR(100),
                                     'CATEGORY',                # 	CATEGORY VARCHAR(100),
                                     'SLUG',                    # 	SLUG VARCHAR(300),
                                     'Origen',                  # 	Origen VARCHAR(50),
                                     'FechaFiltro',             # 	FechaFiltro DATE,           # Origin Date
                                     'FechaCreacion',           # 	FechaCreacion DATE,         # Row insertion Date
                                     'FechaModificacion',       # 	FechaModificacion DATE      # Row modification Date
                                   ],                           # )
                                   defaults = [None] * 13
                                  )

class ScrapsSQL():
    def __init__(self, job_name = None, url = None, primary_key = None, capture_datetime = None, dbg = False):
        self.job_name = job_name
        self.url = url
        self.primary_key = primary_key
        self.capture_datetime = capture_datetime
        self.dbg = dbg

        self.SQL_articles_scrap_v1_cols = list(SQL_articles_scrap_v1_schema.keys())
        self.SQL_articles_scrap_v2_cols = list(SQL_articles_scrap_v2_schema.keys()) # 02/11/2022 during InfobaeScrapper.py dev'ment
        self.SQL_articles_scraps = []

    def stash_row(self, row):
        """
        Stashes a row into SQL_articles_scrap_v1, while computing an UKEY, and
        validating its fields
        TODO: Generalize this. This is only useful for the only table/schema
        defined at present, while the idea is to be able to insert on any of
        a set of defined tables, while keeping the validation automated.
        Arguments:
            row: a SQLArticlesScrapV1Row() namedtuple()
        Returns:
            True: if successful at validating and stashing row
            False: if validation failed
        """
        validated_dict = {}
        
        try:
            for field in list(SQL_articles_scrap_v1_schema.keys()): #[1:]:  # Except UKEY from inspection given that it will be ignored and computed locally
                if SQL_articles_scrap_v1_schema[field]:     # None works as a flag for fields to be trusted...
                    if (len(getattr(row, field)) if getattr(row, field) else 0) > SQL_articles_scrap_v1_schema[field]:
                        # log if a datum exceeds its expected field width
                        logging.warning(f'Field "{field}" exceeds database schema field width of {SQL_articles_scrap_v1_schema[field]}')
                        logging.warning(f'Dumping row attempted to stash and schema:')
                        logging.warning(f'ROW:    {row}')
                        logging.warning(f'SCHEMA: {SQL_articles_scrap_v1_schema}')
                    validated_dict[field] = getattr(row, field)[ : SQL_articles_scrap_v1_schema[field]] if getattr(row, field) else None # Trim to size
                else:
                    validated_dict[field] = getattr(row, field) # FIXME: if no size defined, just trust it...
            # validated_dict['UKEY'] = str(datetime.datetime.now())
            # debug:
            # print("validated_dict['UKEY'] : ", validated_dict['UKEY'])
            self.SQL_articles_scraps.append(SQLArticlesScrapV1Row(**validated_dict))
            return True

        except Exception as e:
            logging.error('Unable to validate and stash ')
            logging.error(f'Dumping row attempted to stash and schema:')
            logging.error(f'ROW:    {row}')
            logging.error(f'SCHEMA: {SQL_articles_scrap_v1_schema}')
            logging.error('Exception information:', exc_info = e)
            return False

    def stash_row_given_schema(self, row, schema, schema_row):  # NOTE: @ 01/11/2022 during InfobaeScrapper.py dev'ment
        "Attempt at quick generalization of above method"
        validated_dict = {}
        
        try:
            for field in list(schema.keys()): #[1:]:  # Except UKEY from inspection given that it will be ignored and computed locally
                if schema[field]:     # None works as a flag for fields to be trusted...
                    if (len(getattr(row, field)) if getattr(row, field) else 0) > schema[field]:
                        # log if a datum exceeds its expected field width
                        logging.warning(f'Field "{field}" exceeds database schema field width of {schema[field]}')
                        logging.warning(f'Dumping row attempted to stash and schema:')
                        logging.warning(f'ROW:    {row}')
                        logging.warning(f'SCHEMA: {schema}')
                    validated_dict[field] = getattr(row, field)[ : schema[field]] if getattr(row, field) else None # Trim to size
                else:
                    validated_dict[field] = getattr(row, field) # FIXME: if no size defined, just trust it...
            # validated_dict['UKEY'] = str(datetime.datetime.now())
            # debug:
            # print("validated_dict['UKEY'] : ", validated_dict['UKEY'])
            self.SQL_articles_scraps.append(schema_row(**validated_dict))
            return True

        except Exception as e:
            logging.error('Unable to validate and stash ')
            logging.error(f'Dumping row attempted to stash and schema:')
            logging.error(f'ROW:    {row}')
            logging.error(f'SCHEMA: {schema}')
            logging.error('Exception information:', exc_info = e)
            return False

    def as_lists_list(self):
        """
        Allows access to what's already stashed in self.SQL_articles_scrap_v1 as a list
        """
        return self.SQL_articles_scraps

    def dump_as_string(self):
        """
        Just for debugging
        """
        dump_str = ', '.join([str(k) + ' (' + str(SQL_articles_scrap_v1_schema[k]) + ')' for k in SQL_articles_scrap_v1_schema]) + '\n'
        for row in self.SQL_articles_scraps:
            dump_str += str(row) + '\n'

        return dump_str    

