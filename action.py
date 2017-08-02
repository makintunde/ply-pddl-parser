class Action(object):
    def __init__(self, action_name):
        self.name = action_name
        self.parameters = []
        self.type_of = {}  # Mapping from variables to types
        self.precondition = None
        self.effect = None
        self.positive_effects = []
        self.negative_effects = []

    def __str__(self):
        return '\n' + 'Name: %s ' % self.name + '\n' + \
               '\n'.join(['Parameters: %s' % str(self.parameters),
                          'Precondition: %s' % str(self.precondition),
                          'Negative Effects: %s' % str(self.negative_effects),
                          'Positive Effects: %s' % str(self.positive_effects)])

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def set_parameters(self, parameters, type_of):
        self.parameters = parameters
        for variable in self.parameters:
            type_of[variable.name] = variable.type

    def type_of(self, variable):
        return self.type_of[variable]

    def set_effect(self, effect):
        self.effect = effect
        and_token, effects = self.effect
        for effect in effects:
            if type(effect) == tuple:  # It is a negative effect.
                not_token, effect = effect
                self.negative_effects.append(effect)
            else:
                self.positive_effects.append(effect)
