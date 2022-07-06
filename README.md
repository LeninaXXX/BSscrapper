## BSscrapper

### Scrapper basado en _Beautiful Soup_

* targets:
	Cada uno tiene por competencia una pagina ("```target```") sobre la que hacer _scrapping_.
	Existe para poder personalizar cada caso.
* tequesters:
	Para cada ```target```, existe un ```requester``` que se ocupa de traer del servidor remoto el/los documento(s) sobre los que se quiere hacer _scrapping_.
	Existe en funcion de las peculiaridades que ese _requesting_ pudiera tener, como bloqueo por numero de solicitudes.
* scrappers:
	Para cada ```target```, existe un ```scrapper```, ajustado a las peculiaridades de cada pagina en cuestion (i.e.: extraer datos de La Nacion vs extraerlos de Ambito Financiero o Infobae no va a ser, en general, igual, dado que la diagramacion de la pagina va a ser diferente).
	Existe en funcion de las peculiaridades de cada *documento* (ya sea *el* documento que un target devuelva, o *los* que interese scrappear) que un ```target``` dado retorne.

#### Ejemplos durante el desarrollo:

 * Ambito Financiero: https://www.ambito.com/
	* ```ambitofinanciero_target``` imported as target
	  * ```ambitofinanciero_requester``` imported as requester
	  * ```ambitofinanciero_scrapper``` imported as scrapper
 * Infobae: https://www.infobae.com
	* ```infobae_target``` imported as target
	  * ```infobae_requester``` imported as requester
	  * ```infobae_scrapper``` imported as scrapper
 * La Nacion: https://www.lanacion.com.ar
	* ```lanacion_target``` imported as target
	  * ```lanacion_requester``` imported as requester
	  * ```lanacion_scrapper``` imported as scrapper

#### Comentarios

Dado *diario*, cada ```diario_target``` especifico, cada ```diario_requester``` especifico, y cada ```diario_scrapper``` especificos, se pueden crear como subclases de clases ```target```, ```requester```, y ```scrapper``` generales.

