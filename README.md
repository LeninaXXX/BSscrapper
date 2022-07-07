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

#### To_Do:

 * Hay metodos en la subclase`lanacion_target` que en una primera aproximacion los puse ahi pensando que iban a tener preculiaridades propias de _La Nacion_, pero que en realidad son completamente genericos, y pueden moverse a la superclase (`target`). Para las subclases solo parecen realmente indispensables cosas como _url_. Si bien tal vez esa logica se podria implementar como instancias de una unica clase, por lo pronto me parece sensato dejarlas por si el scrapping evoluciona a algo mas sofisticado que extraer uno o mas articulos de la portada: representa una buena separacion de tareas, y no complica especialmente las cosas.
 
 * _DBs_:
    * Hace falta definir el _data model_.
	* Por lo pronto se pueden meter _con la pala ancha_ en MongoDB???
	* Preferiria tener la asistencia/supervision de alguien que este familiarizado con las DBs. Dado que conviven bases de datos _de produccion_, mi temor de mandarme un moco es sencillamente mayusculo (aun si creo que no soy tan animal, la precaucion no esta de mas).
	* ... logging...
	* ... to provide ease of debugging?
	* Alertas!!!
	
 * _Ambito Financiero_ & _Infobae_ me quedaron pendientes.
    Decidir un criterio de como individualizar lo que se quiere scrappear *puntualmente* (e.g.: El articulo principal) de manera tal que sea *robustamente repetible* parece deceptively hard, y casi diria que fue lo mas time consuming... es eso o estoy pasando algo obvio por alto y/o encarando mal la cosa.

#### Wishlist:
 
 * Un modo mas inmediato, intuitivo, etc... de 'tantear' ese criterio con el cual individualizar el nodo del tree html del que extraer el scrap.
	Vengo pensando en un script interactivo que permita usar `Beautiful Soup` (u otro scrapper for that matter) de manera interactiva para explorar el texto de un _request_, y que haga mas facil "visualizar" lo que se quiere.
	`Jupyter` garpa... pero se pone verboso rapido y es tal vez demasiado general
 * Idealmente el programa deberia levantar toda la configuracion de archivos externos: Tarea que no parece, ni por asomo, trivial.
 * Dormir (?)