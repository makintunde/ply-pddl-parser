class Name(object):
    def __init__(self, name):
        self.name = name
        self.type = 'object'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name + ' :: ' + self.type