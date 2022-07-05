## BSscrapper
-
### Scrapper basado en _Beautiful Soup_

* Targets:
	Cada uno tiene por competencia una pagina ("```target```") sobre la que hacer _scrapping_.
	Existe para poder personalizar cada caso.
* Requesters:
	Para cada ```target```, existe un ```requester``` que se ocupa de traer del servidor remoto el/los documento(s) sobre los que se quiere hacer _scrapping_.
	Existe en funcion de las peculiaridades que ese _requesting_ pudiera tener, como bloqueo por numero de solicitudes.
* Scrappers:
	Para cada ```target```, existe un ```scrapper```, ajustado a las peculiaridades de cada pagina en cuestion (i.e.: extraer datos de La Nacion vs extraerlos de Ambito Financiero o Infobae no va a ser, en general, igual, dado que la diagramacion de la pagina va a ser diferente).
	Existe en funcion de las peculiaridades de cada *documento* (ya sea *el* documento que un target devuelva, o *los* que interese scrappear) que un ```target``` dado retorne.

#### Ejemplos durante el desarrollo:

 * Infobae: https://www.infobae.com
	* ```infobae_target```
	* ```infobae_requester```
	* ```infobae_scrapper```
 * La Nacion: https://www.lanacion.com.ar
	* ```lanacion_target```
	* ```lanacion_requester```
	* ```lanacion_scrapper```
 * Ambito Financiero: https://www.ambito.com/
	* ```ambitofinanciero_target```
	* ```ambitofinanciero_requester```
	* ```ambitofinanciero_scrapper```


#### Comentarios

	Cada ```target``` especifico 
