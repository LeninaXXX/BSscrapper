# lanacion_scrapper.py -- subclase de scrapper

from scrappers.scrapper import scrapper # make superclass visible

import bs4 as bs
import html5lib

class lanacion_scrapper(scrapper):
	# In here, everything should be in reference to the 'self.soup' 
    # belonging to the superclass. The methods particular to this
    # subclass is where the freedom to scrap particular stuff should lie,
    # i.e.: this is pressuambly gonna be where most of the maintenance
    # tasks will lie in the future
    pass