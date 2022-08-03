# main.py -- main 

import argparse
import os
import logging      # TODO: logging pendiente
import time
from datetime import datetime

from Jobs.AmbitofinancieroJob import AmbitofinancieroJob
from Jobs.ClarinJob import ClarinJob
from Jobs.InfobaeJob import InfobaeJob                       
from Jobs.La100Job import La100Job                       
from Jobs.LanacionJob import LanacionJob
from Jobs.Pagina12Job import Pagina12Job
from Jobs.RadiomitreJob import RadiomitreJob
from Jobs.TNJob import TNJob

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
               'tn'                : TNJob}

epilog = "Jobs disponibles: "
for j in valid_jobs: 
    epilog += valid_jobs[j].__name__[:-3] + ' '
epilog = epilog[:-1]

# cmdline interpretation
cmdline = argparse.ArgumentParser(description = "BSscrapper - Scrapper basado en Beautiful Soup v4", epilog = epilog)
cmdline.add_argument("-d", action = "store_true", dest = "debug", help = "Toggle debugging mode on")
cmdline.add_argument("-j", action = "append", dest = "jobs", help = "Jobs a disparar. Uno por '-j'")

params = cmdline.parse_args()

if params.debug:
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

logging.basicConfig(level = logging.INFO if params.debug == False else logging.DEBUG,
                    encoding = 'utf-8',
                    filename = logfilename, 
                    format = '%(levelname)s:%(asctime)s:%(funcName)s:%(lineno)d - %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S')

# prepare list of jobs to be undertaken
job_list = []
for j in params.jobs:       # filter only valid jobs -- those strings existing as keys in valid
    if j.lower() in valid_jobs:
        job_list.append(valid_jobs[j.lower()](dbg = params.debug))  # switch debugging by passing flag to constructors in the queue - False by default
        logging.info('Adding job ' + valid_jobs[j.lower()].__name__ + ' to queue')
    else:
        print('Job ' + j + ' is unknown!!!')
        logging.warning('Job ' + j + ' is unknown!!!')

if job_list == []:
    print("Ninguno de los trabajos especificados es reconocido"); 
    logging.error("Ninguno de los trabajos especificados es reconocido")
    print("Nada para hacer..."); 
    logging.error("Nada para hacer...")
    print(cmdline.prog, "-h para ver opciones y jobs disponibles")
    exit(0)

logging.info('-' * len("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1]))
logging.info("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1])
logging.info('-' * len("Jobs reconocidos :" + str([j.__class__.__name__ for j in job_list])[1:-1]))

for job in job_list:
    logging.info("Launching job " + job.__class__.__name__)
    job.launch()
    logging.info("Storing job " + job.__class__.__name__ + '\'s collected stuff')
    job.store()

# while True:
#     for job in job_list:
#         logging.info("Launching job " + job.__class__.__name__)
#         job.launch()
#         logging.info("Storing job " + job.__class__.__name__ + '\'s collected stuff')
#         job.store()
#     logging.info('Taking a 2 hour nap...')
#     print('Taking a 1 hour nap...')
#     try:
#         time.sleep(3600)
#     except KeyboardInterrupt:
#         print("Exiting...")
#         exit(0)
#     os.system('cls')