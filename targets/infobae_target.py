# infobae_target.py -- subclase de target

from targets.target import target

from requesters.infobae_requester import infobae_requester as requester
from scrappers.infobae_scrapper import infobae_scrapper as scrapper

class infobae_target(target):
    def __init__(self, url = "https://www.infobae.com"):
        self.url = url
        
    