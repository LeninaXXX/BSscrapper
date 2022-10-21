# main.py -- main 

import argparse
import os
import logging

from collections import namedtuple
from datetime import datetime

# list of available jobs
from Jobs.AmbitofinancieroJob import AmbitofinancieroJob
from Jobs.ClarinJob import ClarinJob
from Jobs.InfobaeJob import InfobaeJob                       
from Jobs.La100Job import La100Job                       
from Jobs.LanacionJob import LanacionJob
from Jobs.Pagina12Job import Pagina12Job
from Jobs.RadiomitreJob import RadiomitreJob
from Jobs.TNJob import TNJob
from Jobs.DatabaseTestJob import DatabaseTestJob

# this dict() is a jump table look-alike used to parse and any new job added to the
# script should be added in here for the command line parser to know what to do.
# FIXME: There should be a more elegant way of doing this, by iterating over a list
#       jobs, and accessing their .__name__ members
valid_jobs = { 'ambitofinanciero'  : AmbitofinancieroJob,
               'clarin'            : ClarinJob,
               'infobae'           : InfobaeJob,
               'la100'             : La100Job,
               'lanacion'          : LanacionJob,
               'pagina12'          : Pagina12Job,
               'radiomitre'        : RadiomitreJob, # me habia comido este job. Costo poco agregarlo (45"). Buen approach...
               'tn'                : TNJob,
               'databasetest'      : DatabaseTestJob,
               }

epilog = "Jobs disponibles:"
for j in valid_jobs: 
    epilog += ' ' + valid_jobs[j].__name__[:-3]

# cmdline interpretation
cmdline = argparse.ArgumentParser(description = "BSscrapper - Scrapper basado en Beautiful Soup v4", epilog = epilog)

cmdline.add_argument("-dc", action = "store_true", dest = "debug_commit", 
                     help = "Toggle debugging mode on for database commits -- Database commits get tagged")
cmdline.add_argument("-dp", action = "store_true", dest = "debug_program", 
                     help = "Toggle debugging mode on for program. Logger mode gets set to DEBUG")
cmdline.add_argument("-f", action = "store_true", dest = "file_commit", 
                     help = "Commit result of scrapping to file, not to database. Here for debugging purposes")
cmdline.add_argument("-j", action = "append", dest = "jobs", 
                     help = "Jobs a disparar. Uno por '-j'")

params = cmdline.parse_args()   # TODO: Available params and what are they intended for:
                                #   debug_commit:   Database commits should get tagged as DBG
                                #   debug_program:  Program get much more verbose when it comes to logging
                                #   file_commit:    No commits to database. Dump to file for inspection instead
                                #   jobs:           list of jobs to be executed

# TODO: to implement debugging switches as a 'bundle' instead of loose switches, for brevity and clarity
#       pack everything into a named- (for clarity) -tuple (for brevity)
dbg = namedtuple('DebugTuple', ['commit', 'program', 'file_commit']) 
(dbg.commit, dbg.program, dbg.file_commit) = (params.debug_commit, params.debug_program, params.file_commit)

if params.debug_program:
    print("cmdline:\n\t", cmdline)
    print()
    print("params:\n\t", params)

if not params.jobs:
    print("Nada para hacer...")
    print(cmdline.prog, "-h para ver opciones y jobs disponibles")
    exit(0)

# TODO: Logging config
# Logging Config -- Comments from The Python Library Reference Release 3.9.4 by Guido van Rossum and the Python development team
d = datetime.now()                                          # "datetime.now() : Return the current local date and time" [Page 183]
# log path at ./logs/<year-month-day> 
logpath = os.getcwd() + "/logs/" + d.strftime('%Y%m%d')     # "os.getcwd() : Returns a string representing the current working directory" [Page 568]
                                                            # "datetime.strftime() : Return a string representing the date and time, controlled by an explicit format string.
                                                            # For a complete list of formatting directives, see strftime() and strptime() Behavior [Page 203]" [Page 191]
os.makedirs(logpath, exist_ok=True)                         # "os.makedirs() : Recursive directory creation function [...]" 
                                                            # "If exists_ok is False (the default), an FileExistsError ir raised if the target directory already exists"
                                                            # [Page 570]

logfilename = logpath + "/" + d.strftime('%Y%m%d%H%M%S') +  ".log"
print('Logging in: ' + logfilename + '\n')

logging.basicConfig(level = logging.INFO if params.debug_program == False else logging.DEBUG,
                    encoding = 'utf-8',
                    filename = logfilename, 
                    format = '%(levelname)s:%(asctime)s:%(funcName)s:%(lineno)d - %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S')

# prepare list of jobs to be undertaken
job_list = []
for j in params.jobs:       # filter only valid jobs -- those strings existing as keys in valid
    if j.lower() in valid_jobs:
        job_list.append(valid_jobs[j.lower()](dbg = params.debug_commit))  # switch debug & file_commit flags. False by defaults
        if params.debug_program:
            logging.info("Database commits to be flagged as debug")
        logging.info('Adding job ' + valid_jobs[j.lower()].__name__ + ' to queue')
    else:
        print('Job ' + j + ' is unknown!!!')
        logging.warning('Job ' + j + ' is unknown!!!')

if job_list == []:
    logging.error("Ninguno de los trabajos especificados es reconocido")
    logging.error("Nada para hacer...")
    print("Ninguno de los trabajos especificados es reconocido")
    print("Nada para hacer..."); 
    print(cmdline.prog, "-h para ver opciones y jobs disponibles")
    exit(0)

logging.info('-' * len("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1]))
logging.info("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1])
logging.info('-' * len("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1]))
print('-' * len("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1]))
print("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1])
print('-' * len("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1]))

for job in job_list:
    logging.info("Launching job " + job.__class__.__name__)
    print("Launching job " + job.__class__.__name__)
    job.launch()
    logging.info("Storing job " + job.__class__.__name__ + '\'s collected stuff')
    print("Storing job " + job.__class__.__name__ + '\'s collected stuff')
    job.store(params.file_commit)   # if commit is done to a file the only one concerned is the one what stores

