"""
Parser for PDDL domain files.
"""

import ply.yacc as yacc

# Get the token map from the lexer. Required.
from pddl_lex import tokens


class Domain(object):

    def __init__(self, name):
        self.name = name
        self.definition = None
        self.types = None
        self.components = []
        self.requirements = []
        self.predicates = {}
        self.actions = {}

    def __str__(self):
        return '\n'.join(['Name: %s' % self.name,
                          'Requirements: %s' % str(self.requirements),
                          'Predicates: %s' % str(self.predicates),
                          'Actions: %s' % str(self.actions.values())])

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

    def set_components(self, components):
        for k, v in components:
            if k == ':requirements':
                self.requirements = v
            elif k == ':types':
                self.types = v
            elif k == ':predicates':
                self.predicates = v


class Action(object):
    def __init__(self, action_name):
        self.name = action_name
        self.parameters = []
        self.precondition = None
        self.effect = None

    def __repr__(self):
        return '\n' + 'Name: %s ' % self.name + '\n' + \
               '\n'.join(['Parameters: %s' % str(self.parameters),
                          'Precondition: %s' % str(self.precondition),
                          'Effect: %s' % str(self.effect)])

    def add_parameter(self, parameter):
        self.parameters.append(parameter)


def p_domain(p):
    'domain_declr : LPAREN DEFINE domain_def RPAREN'
    p[0] = p[3]


def p_domain_def(p):
    '''domain_def : LPAREN DOMAIN ID RPAREN domain_components actions_declr'''
    pddl_domain = Domain(p[3])
    pddl_domain.set_components(p[5])
    pddl_domain.actions = p[6]
    p[0] = pddl_domain


def p_domain_components(p):
    '''domain_components : domain_components domain_component
                         | domain_component'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_domain_component(p):
    '''domain_component : requirements_declr
                        | types_declr
                        | predicates_declr'''
    p[0] = p[1]


def p_requirements_declr(p):
    '''requirements_declr : LPAREN REQUIREMENTS requirements_def RPAREN'''
    p[0] = (p[2], p[3])


def p_types_declr(p):
    '''types_declr : LPAREN TYPES types_def RPAREN'''
    p[0] = (p[2], p[3])


def p_predicates_declr(p):
    'predicates_declr : LPAREN PREDICATES predicates_def RPAREN'
    p[0] = (p[2], p[3])


def p_actions_declr(p):
    '''actions_declr : actions_declr action_declr 
                     | action_declr'''
    if len(p) == 2 and p[1]:
        p[0] = {p[1].name: p[1]}
    elif len(p) == 3:
        p[0] = p[1]
        p[0][p[2].name] = p[2]


def p_action_declr(p):
    '''action_declr : LPAREN ACTION ID action_parameters_def precondition_def effect_def RPAREN'''
    new_action = Action(p[3])
    new_action.parameters = p[4]
    new_action.precondition = p[5]
    new_action.effect = p[6]
    p[0] = new_action


def p_action_parameters_def(p):
    '''action_parameters_def : PARAMETERS LPAREN parameters_def RPAREN'''
    p[0] = p[3]


def p_precondition_def(p):
    '''precondition_def : PRECONDITION precondition_declr'''
    p[0] = p[2]


def p_effect_def(p):
    '''effect_def : EFFECT effect_declr'''
    p[0] = p[2]


def p_effect_declr(p):
    '''effect_declr : LPAREN AND effect_expr RPAREN
                    | LPAREN OR effect_expr RPAREN
                    | LPAREN NOT predicate_def RPAREN
                    | predicate_def'''
    if len(p) == 5:
        p[0] = (p[2], p[3])
    else:
        p[0] = ('PRED', p[1])


def p_effect_expr(p):
    '''effect_expr : effect_expr LPAREN NOT predicate_def RPAREN
                   | effect_expr predicate_def
                   | predicate_def'''
    if len(p) == 6:
        p[1].append((p[3], p[4]))
        p[0] = p[1]
    elif len(p) == 3:
        p[1].append(('PRED', p[2]))
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [('PRED', p[1])]


def p_precondition_declr(p):
    '''precondition_declr : LPAREN AND precondition_expr RPAREN
                          | LPAREN OR precondition_expr RPAREN
                          | predicate_def'''
    if len(p) == 5:
        p[0] = (p[2], p[3])
    else:
        p[0] = ('PRED', p[1])


def p_precondition_expr(p):
    '''precondition_expr : precondition_expr predicate_def
                         | predicate_def'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_requirements_def(p):
    '''requirements_def : requirements_def requirement
                        | requirement'''
    if len(p) == 2 and p[1]:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]


def p_types_def(p):
    '''types_def : types_def ID
                 | ID'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]


def p_requirement(p):
    '''requirement : STRIPS 
                   | EQUALITY 
                   | TYPING 
                   | ADL'''
    p[0] = p[1]


def p_predicates_def(p):
    '''predicates_def : predicates_def predicate_def
                      | predicate_def'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]


class Predicate(object):
    def __init__(self, predicate_name):
        self.name = predicate_name
        self.parameters = []

    def __repr__(self):
        return str((self.name, self.parameters))

    def add_parameter(self, parameter):
        self.parameters.append(parameter)


def p_predicate_def(p):
    '''predicate_def : LPAREN ID parameters_def RPAREN'''

    predicate_name = p[2]
    new_predicate = Predicate(predicate_name)
    new_predicate.parameters = p[3]
    p[0] = new_predicate


def p_parameters_def(p):
    '''parameters_def : parameters_def PARAMETER
                      | PARAMETER'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]


# def p_parameter_def(p):
#     '''parameter_def : PARAMETER DASH ID
#                      | PARAMETER'''
#     if len(p) == 3:
#         p[0] = (p[1], p[3])
#     else:
#         p[0] = (p[1], 'object')


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()


def main():
    import sys

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        # Remove single line comments
        data = f.read()

    result = parser.parse(data, tracking=True)
    print(result)

if __name__ == '__main__':
    main()

