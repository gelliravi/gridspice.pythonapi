# Intro To Python:  Modules
# book.py

import httplib
import urllib
import config

class Account:

    """
      The GridSpice account object contains the credentials for communication with the model server
    """
    def __init__(self, email = "null"):
                if (email != "null") :
                        conn = httplib.HTTPConnection(config.URL)
                        conn.request("GET", "/users/login.json"
                                + "?"
                                + "email=" + email);
                        res = conn.getresponse()
                        if (res.status == 200 and res.reason == "OK"):
                                data = res.read()
                                id = int(data)
                                if (id > 0):
                                        self._id = id
                                        self._email = email
                                        self._currentProject = None
                                        print "Welcome " + email + "!"
                                else:   
                                        conn.close()
                                        raise ValueError("'" + email + "'"  + " is not a valid email address.")
                        conn.close()

    def getProjects():
        """
           Gets the projects associated with this account
        """

    def storeProject(project):
	"""
	   Stores a new project associated with this account
	"""

    def updateProject(project):
	"""
	   Updates a project associated with this account
	"""

    def deleteProject(project):
	"""
	   Deletes a project associated with this account
	"""

    def logout():
        """
           Logs out the current user
        """
        return;
