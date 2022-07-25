# Requester.py -- general superclass

# this module should only be visible to Job.py, that is, to class Job and its subclasses <target>Job

import requests

class Requester():
    def __init__(self, url, headers = None, params = None):
        self.url = url          
        self.headers = headers
        self.params = params
        self.ret = None

    def set_url(self, url):
        self.url = url
    
    def set_header(self, header):
        self.header = header
        
    def set_params(self, params):
        self.params = params
    
    def go_fetch(self):
        try:
            self.ret = requests.get(self.url, headers = self.headers, params = self.params)
        except:
            self.ret = DummyExceptedReq()
        
    def payload(self):
        return self.ret
        
    def payload_text(self):
        return self.ret.text if self.ret != None else None

    def payload_reason(self):
        return self.ret.reason if self.ret != None else None
	
    def payload_status_code(self):
        return self.ret.status_code if self.ret != None else None

    def payload_apparent_encoding(self):
        return self.ret.apparent_encoding if self.ret != None else None

    def payload_content(self):
        return self.ret.content if self.ret != None else None
		
    def payload_elapsed(self):
        return self.ret.elapsed if self.ret != None else None

class DummyExceptedReq():
    def __init__(self):
        self.text = ""
        self.reason = "!!!EXCEPTION DURING REQUEST!!!"
        self.status_code = None
        self.apparent_encoding = None
