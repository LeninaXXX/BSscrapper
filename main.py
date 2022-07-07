# main.py -- main xD

import logging  # TODO: logging pendiente
import sys      # Para hacer argparsing a lo bruto

from targets.ambitofinanciero_target import ambitofinanciero_target     # TODO: Segunda prioridad
from targets.infobae_target import infobae_target                       
from targets.lanacion_target import lanacion_target

def ls(x = None):
    if x:
        return [elem for elem in dir(x) if elem[:2] != '__']
    else:
        return dir()
    
# Todo esto es una asquerosidad deforme para salir del paso que tiene a ser extirpada
#    y reemplazada por un apropiado manejo de parametros en command line
# 
# args = list(set(sys.argv[1:]))      # deduplicar argumentos
# for arg in args:
#     if arg == "AmbitoFinanciero":
#         ambitofinanciero = ambitofinanciero_target()    # creo job "Ambito Financiero"
#         ambitofinanciero.launch()                       # ... lanzo job : request + scrap
#         #
#         #                                                 ... inspecciono el resultado si 
#         #                                                 ... asi lo quiero (placeholder)
#         #
#         ambitofinanciero.store()                        # ... commiteo a la database
#     
#     elif arg == "Infobae":
#         infobae = infobae_target()                      # ... job "Infobae"
#         infobae.launch()                                # ... lanzo
#         #
#         # ... inspecciono, si asi lo quiero (placeholder)
#         #
#         infobae.store()                                 # ... 
#     
#     elif arg == "LaNacion":
#         lanacion = lanacion_target()                    # ... job "La Nacion"
#         lanacion.launch()                               # ... lanzo job...
#         #
#         # ... inspecciono, si asi lo quiero (placeholder)
#         #
#         lanacion.store()                                # ... 
#     else:
#         print('"' + arg + '"', "no es un target valido")    # ... y coso (?)
#         # continue

# ambitofinanciero = ambitofinanciero_target()
# infobae = infobae_target()

lanacion = lanacion_target()
# lanacion.launch()               
# lanacion.store()


