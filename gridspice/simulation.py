# Intro To Python:  Modules
# book.py

class Simulation:

    """
      The GridSpice simulation object contains a project's simulation results
    """
    def __init__(self, id, projectId, result, timeStamp):
        self.id = id
        self.projectId = projectId
        self.result = result
        self.timeStamp = timeStamp
        


