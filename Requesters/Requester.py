# Requester.py -- general superclass

# this module should only be visible to Job.py, that is, to class Job and its subclasses <target>Job

import requests
import logging

class Requester():
    def __init__(self, job_name = None, url = None, headers = None, params = None, dbg = False):
        self.job_name = job_name
        self.url = url        
        self.headers = headers
        self.params = params
        self.ret = None
        self.dbg = dbg
        print("Requester :", self.job_name, "/ debug_commit :", self.dbg)

    def set_job_name(self, job_name):
        self.job_name = job_name

    def set_url(self, url):         # same as setting url when constructing
        self.url = url
    
    def set_header(self, header):   # same as setting headers when constructing
        self.header = header
        
    def set_params(self, params):   # same as setting params when constructing
        self.params = params
    
    def go_fetch(self):
        try:
            self.ret = requests.get(self.url, headers = self.headers, params = self.params)
        except Exception as e:
            logging.exception("Something went wrong when trying to fetch: " + self.job_name)
            logging.exception("Something went wrong when trying to fetch: " + self.url)
            logging.exception("------------------------------------------")
            logging.exception(str(self.ret))
            logging.exception("------------------------------------------")
            self.ret = DummyExceptedReq()   # TODO: This should be replaced by proper exception propagation
        
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

class DummyExceptedReq():       # FIXME: this kruft is fucking disgusting. This should
    def __init__(self):         #   be properly managed with true exceptions!!!
        self.text = None
        self.reason = "!!!EXCEPTION DURING REQUEST!!!"
        self.status_code = None
        self.elapsed = None             # Datamodel 2nd Iteration
        self.encoding = None            # Datamodel 2nd Iteration
        self.apparent_encoding = None