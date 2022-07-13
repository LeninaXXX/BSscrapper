# main.py -- main xD

import argparse
import logging      # TODO: logging pendiente
# import sys        # Para hacer argparsing a lo bruto

from jobs.ambitofinanciero_job import ambitofinanciero_job     # TODO: Segunda prioridad
from jobs.infobae_job import infobae_job                       
from jobs.lanacion_job import lanacion_job

cmdline = argparse.ArgumentParser(description = "BSscrapper - Scrapper basado en Beautiful Soup v4")
cmdline.add_argument("-j", action = "append", dest = "jobs", help = "Job a iniciar")
cmdline.add_argument("-l", action = "store", dest = "loglvl", help = "loglvl: Nivel de detalle de logging", default = logging.INFO)  # TODO: logging pendiente
params = cmdline.parse_args()

# TODO: Logging config
# Logging por default a nivel INFO
# Permitir, al menos, nivel INFO y DEBUG

lanacion = lanacion_job()


