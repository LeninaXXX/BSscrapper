# main.py -- main 

import argparse
import logging      # TODO: logging pendiente
import time

from Jobs.AmbitofinancieroJob import AmbitofinancieroJob
from Jobs.InfobaeJob import InfobaeJob                       
from Jobs.LanacionJob import LanacionJob

cmdline = argparse.ArgumentParser(description = "BSscrapper - Scrapper basado en Beautiful Soup v4")
cmdline.add_argument("-j", action = "append", dest = "jobs", help = "Job a iniciar")
cmdline.add_argument("-l", action = "store", dest = "loglvl", help = "loglvl: Nivel de detalle de logging", default = logging.INFO)  # TODO: logging pendiente
params = cmdline.parse_args()

# TODO: Logging config

# 
# while True:
#     infobae = InfobaeJob()
#     infobae.launch()
#     infobae.store()
#     print("Taking a 5 minute nap...")
#     time.sleep(5*60)

infobae = InfobaeJob()