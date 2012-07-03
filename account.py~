# Intro To Python:  Modules
# book.py

"""
Class:  Book( title, author, keywords )
Each book object takes a title, optional author, and optional keywords.
"""
class Book:
    def __init__(self, title, author="Unknown", keywords=[]):
        """
        Books take three arguments to their constructor
        The first and only required argument is the title,
        followed by the optional arguments, author, and a list
        of keywords that can be used to look up a specific book.
        """
        self.title = title
        self.author = author
        self.keywords = keywords

    def setTitle(self, title):
        """
        Takes one argument, the title of the book object.
        """
        self.title = title

    def setAuthor(self, author):
        """
        Takes one argument, the author of the book object.
        """
        self.author = author

    def setKeywords(self, keywords):
        """
        Takes one argument, the keywords list for this book object.
        """
        self.keywords = keywords

        # Overload print operation, print a specific format for books.
    def __str__(self):
        s  = "+++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        s += "+" + self.title + "\n"
        s += "+" + self.author +"\n"
        s += "+" + str(self.keywords) + "\n"
        s += "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return s
