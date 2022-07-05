#!/usr/bin/python
import validators       # para validar urls
import sys              # para acceder parametros en linea de comandos
import os               # cuz why not?
import requests
import bs4

from pprint import pprint

if len(sys.argv) <= 1:
    print("Uso:")
    print("\t", os.path.split(sys.argv[0])[-1], " <lista de archivos>", sep='')
    print("\tdonde <lista de archivos> son archivos conteniendo una URL valida por linea", sep='')
    exit(0)

args = []; 
for elem in sys.argv[1:]: 
    if elem not in args: args.append(elem)

valid_files = False                 # assume all files are invalid
urls = []
for arg in args:
    try:
        with open(arg, 'r') as f:
            valid_files = valid_files or True   # if at least one file is valid, there are valid files
            lines = enumerate([l.strip() for l in f.readlines()], start=1)    # limpio y enumero lineas
           
            for l in lines:
                if validators.url(l[1]):
                    urls.append(l[1])
                elif l[1][0] != '#':
                    print("%s : %d -- URL Invalida" % (arg, l[0]))
    except FileNotFoundError:
        print("Archivo:", sys.argv[1], "no existe!")
        continue

if not valid_files or urls == []:   # if nothing to do, gtfoh and whine
    print("Nada que hacer ...")
    exit(1)     # errorlvl == 1

