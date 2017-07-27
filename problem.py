class Problem(object):
    def __init__(self, name):
        self.name = name
        self.requirements = []
        self.types = []
        self.objects = []
        self.init_state = []
        self.goal_state = []

    def __str__(self):
        details = '\n'.join(['Name: %s' % self.name,
                             'Requirements: %s' % str(self.requirements),
                             'Types: %s' % str(self.types),
                             'Objects: %s' % str(self.objects),
                            ])

        details += '\n' + 'Initial state: '

        for predicate in self.init_state:
            details += '\n' + str(predicate)

        details += '\n'

        details += '\n' + 'Goal state: '

        for predicate in self.goal_state:
            details += '\n' + str(predicate)

        details += '\n'
        return details

    def set_components(self, components):
        for k, v in components:
            if k == ':requirements':
                self.requirements = v
            elif k == ':types':
                self.types = v
            elif k == ':objects':
                self.objects = v