# main.py -- main xD

import argparse
import logging      # TODO: logging pendiente
# import sys        # Para hacer argparsing a lo bruto

from Jobs.AmbitofinancieroJob import AmbitofinancieroJob     # TODO: Segunda prioridad
from Jobs.InfobaeJob import InfobaeJob                       
from Jobs.LanacionJob import LanacionJob

cmdline = argparse.ArgumentParser(description = "BSscrapper - Scrapper basado en Beautiful Soup v4")
cmdline.add_argument("-j", action = "append", dest = "jobs", help = "Job a iniciar")
cmdline.add_argument("-l", action = "store", dest = "loglvl", help = "loglvl: Nivel de detalle de logging", default = logging.INFO)  # TODO: logging pendiente
params = cmdline.parse_args()

# TODO: Logging config
# Logging por default a nivel INFO
# Permitir, al menos, nivel INFO y DEBUG

# lanacion = LanacionJob()

ambito = AmbitofinancieroJob()
# ambito.launch()


