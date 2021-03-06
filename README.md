# BSscrapper

## Scrapper basado en _Beautiful Soup_

* jobs:
      Cada uno tiene por competencia una pagina ("_target_") sobre la que hacer _scrapping_.
    Existe para poder personalizar cada caso.
* requesters:
	  Para cada ```job```, existe un ```requester``` que se ocupa de traer del servidor remoto el/los documento(s) sobre los que se quiere hacer _scrapping_.
	Existe en funcion de las peculiaridades que ese _requesting_ pudiera tener, como bloqueo por numero de solicitudes.
* scrappers:
	  Para cada ```job```, existe un ```scrapper```, ajustado a las peculiaridades de cada pagina en cuestion (i.e.: extraer datos de La Nacion vs extraerlos de Ambito Financiero o Infobae no va a ser, en general, igual, dado que la diagramacion de la pagina va a ser diferente).
	Existe en funcion de las peculiaridades de cada *documento* que un _target_ dado retorne (ya sea *el* o *los* documentos que se recuperen de un _target_ e interese scrappear).

### Ejemplos durante el desarrollo:

 * Ambito Financiero: https://www.ambito.com/
	* ```ambitofinanciero_job``` imported as job
	  * ```ambitofinanciero_requester``` imported as requester
	  * ```ambitofinanciero_scrapper``` imported as scrapper
 * Infobae: https://www.infobae.com
	* ```infobae_job``` imported as job
	  * ```infobae_requester``` imported as requester
	  * ```infobae_scrapper``` imported as scrapper
 * La Nacion: https://www.lanacion.com.ar
	* ```lanacion_job``` imported as job
	  * ```lanacion_requester``` imported as requester
	  * ```lanacion_scrapper``` imported as scrapper

### Comentarios

Dado *diario*, cada ```diario_job``` especifico, cada ```diario_requester``` especifico, y cada ```diario_scrapper``` especificos, se pueden crear como subclases de clases ```job```, ```requester```, y ```scrapper``` generales.

## Uso

Clonar el repositorio,

	git clone https://github.com/LeninaXXX/BSscrapper

crear un _virtual environment_,

	python -m venv .venv

activar el virtual environment,

	.venv\Scripts\Activate.bat

instalar paquetes requeridos; se van a instalar al virtual environment, en `.venv`,

	pip install -r requirements.txt

Hecho esto, el paquete deberia estar listo para ser usado:

	python main.py -j <job/s>

Donde ```job/s``` es uno o mas trabajos validos:

## To_Do:

* El _DataModel_ es medio un moving target y esta pendiente de actualizacion...

 ~~* Hay metodos en la subclase `lanacion_job` que en una primera aproximacion los puse ahi pensando que iban a tener preculiaridades propias de _La Nacion_, pero que en realidad son completamente genericos, y pueden moverse a la superclase (`job`). Para las subclases solo parecen realmente indispensables cosas como _url_. Si bien tal vez esa logica se podria implementar como instancias de una unica clase, por lo pronto me parece sensato dejarlas por si el scrapping evoluciona a algo mas sofisticado que extraer uno o mas articulos de la portada: representa una buena separacion de tareas, y no complica especialmente las cosas.~~
 
 * _DBs_:
    * Hace falta definir el _data model_.
	~~* Por lo pronto se pueden meter _con la pala ancha_ en MongoDB???~~
	~~* Preferiria tener la asistencia/supervision de alguien que este familiarizado con las DBs. Dado que conviven bases de datos _de produccion_, mi temor de mandarme un moco es sencillamente mayusculo (aun si creo que no soy tan animal, la precaucion no esta de mas).~~
	* ... logging...
	* ... to provide ease of debugging at database insertion level
	* Alertas!!!
	
 * _Ambito Financiero_ & _Infobae_ me quedaron pendientes.
    Decidir un criterio de como individualizar lo que se quiere scrappear *puntualmente* (e.g.: El articulo principal) de manera tal que sea *robustamente repetible* parece deceptively hard, y casi diria que fue lo mas time consuming... es eso o estoy pasando algo obvio por alto y/o encarando mal la cosa.

 * _Selenium_:
	El scrapping de targets como _La Nacion_ parecen volver inevitable el uso de _Selenium/WebDriver_

## Wishlist:
 
 * Un modo mas inmediato, intuitivo, etc... de 'tantear' ese criterio con el cual individualizar el nodo del tree html del que extraer el scrap.
	Vengo pensando en un script interactivo que permita usar `Beautiful Soup` (u otro scrapper for that matter) de manera interactiva para explorar el texto de un _request_, y que haga mas facil "visualizar" lo que se quiere.
	`Jupyter` garpa... pero se pone verboso rapido y es tal vez demasiado general
 * Idealmente el programa deberia levantar toda la configuracion de archivos externos: Tarea que no parece, ni por asomo, trivial.
 * Dormir (?)

---
## Sitios "Suyos"
 * Ambito Financiero: https://www.ambito.com/
 * Infobae: https://www.infobae.com
 * La Nacion: https://www.lanacion.com.ar
 
## Sitios "Nuestros"
 * La 100 Radio ( https://radiomitre.cienradios.com )

---
## DataModels
### SQL
	id
	captureDatetime
	name
	url
	mainArticle
	mainArticleCategory
	mainArticleLead
	nArticles
	nEconomics
	nPolitics
	nSociety
	nSports
	nPolice
	nOthers

### MongoDB

	mongodb_document {'id': ..., 'rawData': ..., 'annotations': }
		id : str()
		rawData : dict()
			requests_text : str()
			requests_reason : str()
			requests_status_code : str()		# type(req.status_code) == int
			requests_apparent_encoding : str()
		annotations : {}
			main_article: dict()
			articles : list()
				article_1 : dict()
				article_2 : dict()
				...		
				article_i : dict()
					title : str()
					slug : str()
					category : str()
					photo : {}
						location : {}
							abs_loc :
							rel_loc :
						size : {}
							abs_size : 
							rel_size : 
				...
				article_n : dict()


 How to commit this into MongoDB: 

https://www.mongodb.com/compatibility/json-to-mongodb#how-to-import-json-into-mongodb-using-python
---
## Log

pyodbc : pyodbc 4.0.32 => pyodbc 4.0.34
MongoDB_doc separado en MongoDB_raw_doc & MongoDB_clean_doc.
    MongoDB_raw_doc to be commited to _RAWDATA Collection_
    MongoDB_clean_doc to be commited to _CLEANSED Collection_
