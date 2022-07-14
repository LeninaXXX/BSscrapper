# requester.py -- clase general

# este modulo deberia ser solo visible a target

import requests

class Requester():
    def __init__(self, url, headers = None, params = None):
        # in // "target"
        self.url = url          
        self.headers = headers
        self.params = params
        # out // "the spoils"
        # self.pload = None     
        #    full 'requests' response -- 'pload' instead of 'payload' to avoid namespace 
        #    collision turns out that no es conveniente definirlo hasta fetchear por lo 
        #    pronto, llamar a 'payload' o 'payload_text' automaticamente triggerea las 
        #    llamadas apropiadas para que el return este definido.
    def set_url(self, url):
        self.url = url
    
    def set_header(self, header):
        self.header = header
        
    def set_params(self, params):
        self.params = params
    
    def go_fetch(self):
        self.pload = requests.get(self.url, headers = self.headers, params = self.params)
        
    # this makes sense for the generality's sake and _the future_
    # i.e.: en algun punto puede interesarme manosear el pload ("payload")
    def payload(self):
        try:
            return self.pload
        except NameError:
            self.go_fetch()
            return self.pload
        
    # ... for the sake of straightforwardness because it's what BeautifulSoup wants
    def payload_text(self):
        try:
            return self.pload.text  # return self.payload().text?
        except AttributeError:
            self.go_fetch()
            return self.pload.text  # return self.payload().text?    