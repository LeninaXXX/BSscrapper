# requester.py -- clase general

# este modulo deberia ser solo visible a target

import requests

class requester():
    def __init__(self, url, headers = None, params = None):
        # in // "target"
        self.url = url          
        self.headers = headers
        self.params = params
        # out // "the spoils"
        self.pload = None     # gonna be a full 'requests' response
    
    def set_url(self, url):
        self.url = url
    
    def set_header(self, header):
        self.header = header
        
    def set_params(self, params):
        self.params = params
    
    def go_fetch(self):
        self.pload = requests.get(self.url, 
                                    headers = self.headers, 
                                    params = self.params)
        
    # this makes sense for the sake of generality and _the future_
    def payload(self):
        try:
            return self.pload
        except NameError:
            self.go_fetch()
            return self.pload
        
    # ... for the sake of straightforwardness because it's what BeautifulSoup wants
    def payload_text(self):
        try:
            return self.pload.text
        except AttributeError:
            self.go_fetch()
            return self.pload.text      