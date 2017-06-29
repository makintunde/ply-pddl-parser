class Predicate(object):
    def __init__(self, predicate_name):
        self.name = predicate_name
        self.variables = []

    def __repr__(self):
        return str((self.name, self.variables))

    def add_parameter(self, parameter):
        self.variables.append(parameter)