# ambitofinanciero_target.py -- subclase de target

from targets.target import target

from requesters.ambitofinanciero_requester import ambitofinanciero_requester as requester
from scrappers.ambitofinanciero_scrapper import ambitofinanciero_scrapper as scrapper

class ambitofinanciero_target(target):
    def __init__(self, url = "https://www.ambito.com"):
        self.url = url
    