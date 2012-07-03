# Intro To Python:  Modules
# book.py

class Project:

    """
      The GridSpice project object keeps track of the group of models to be simulated, as well as global settings
      which pertain to all models in the simulation.
    """
    def __init__(self, title, author="Unknown", keywords=[]):
        self.title = title
        self.author = author
        self.keywords = keywords

