class Action(object):
    def __init__(self, action_name):
        self.name = action_name
        self.parameters = []
        self.type_of = {}  # Mapping from variables to types
        self.precondition = None
        self.effect = None

    def __str__(self):
        return '\n' + 'Name: %s ' % self.name + '\n' + \
               '\n'.join(['Parameters: %s' % str(self.parameters),
                          'Precondition: %s' % str(self.precondition),
                          'Effect: %s' % str(self.effect)])

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def set_parameters(self, parameters, type_of):
        self.parameters = parameters
        for variable in self.parameters:
            type_of[variable.name] = variable.type

    def type_of(self, variable):
        return self.type_of[variable]
