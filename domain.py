class Domain(object):

    def __init__(self, name):
        self.name = name
        self.definition = None
        self.types = None
        self.components = []
        self.constants = []
        self.requirements = []
        self.predicates = {}
        self.action_map = {}
        self.actions = []

    def __str__(self):
        details = '\n'.join(['Name: %s' % self.name,
                             'Requirements: %s' % str(self.requirements),
                             'Types: %s' % str(self.types),
                             'Constants: %s' % str(self.constants),
                             'Predicates: %s' % str(self.predicates)])

        details += '\n' + 'Actions: '

        for action in self.actions:
            details += '\n' + str(action)

        details += '\n'

        return details

    def set_definition(self, definition):
        self.definition = definition

    def set_name(self, name):
        self.name = name

    def add_requirement(self, requirement):
        self.requirements.append(requirement)

    def add_action(self, action_name, action):
        self.actions[action_name] = action

    def add_predicate(self, predicate_name, predicate):
        self.predicates[predicate_name] = predicate

    def set_components(self, components, type_of):
        for k, v in components:
            if k == ':requirements':
                self.requirements = v
            elif k == ':types':
                self.types = v
            elif k == ':predicates':
                self.predicates = v
            elif k == ':constants':
                self.constants = v
                for variable in v:
                    type_of[variable.name] = variable.type
