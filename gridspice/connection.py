import config
import httplib
import urllib

STATIC_CONNECTION = None

def create():
		global STATIC_CONNECTION
		if (STATIC_CONNECTION is None):
			STATIC_CONNECTION = httplib.HTTPConnection(config.URL)
			print ("Created a new connection.")
		return STATIC_CONNECTION
			
