"""
Parser for PDDL domain files.
"""

import ply.yacc as yacc

# Get the token map from the lexer. Required.
from pddl_lex import tokens

from action import Action
from domain import Domain
from name import Name
from predicate import Predicate
from variable import Variable


def p_domain(p):
    'domain_declr : LPAREN DEFINE domain_def RPAREN'
    p[0] = p[3]

type_of = {}


def p_domain_def(p):
    '''domain_def : LPAREN DOMAIN ID RPAREN domain_components actions_declr'''
    pddl_domain = Domain(p[3])
    pddl_domain.set_components(p[5], type_of)
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
                        | predicates_declr
                        | constants_declr'''
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



def p_constants_declr(p):
    '''constants_declr : LPAREN CONSTANTS typed_name_list RPAREN'''
    p[0] = (p[2], p[3])


def p_actions_declr(p):
    '''actions_declr : actions_declr action_declr 
                     | action_declr'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_action_declr(p):
    '''action_declr : LPAREN ACTION ID action_parameters_def precondition_def effect_def RPAREN'''
    new_action = Action(p[3])
    new_action.set_parameters(p[4], type_of)
    new_action.precondition = p[5]
    new_action.effect = p[6]
    p[0] = new_action


def p_action_parameters_def(p):
    '''action_parameters_def : PARAMETERS LPAREN typed_variable_list RPAREN
                            | PARAMETERS LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = []


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
                   | LPAREN NOT predicate_def RPAREN
                   | predicate_def'''
    if len(p) == 6:
        p[1].append((p[3], p[4]))
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = [(p[2], p[3])]
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_precondition_declr(p):
    '''precondition_declr : LPAREN AND precondition_expr RPAREN
                          | LPAREN OR precondition_expr RPAREN
                          | predicate_def'''
    if len(p) == 5:
        p[0] = (p[2], p[3])
    else:
        p[0] = p[1]


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


# If we have any typed names, they must come first.
def p_typed_name_list(p):
    '''typed_name_list : name_list
                       | single_type_name_lists
                       | single_type_name_lists name_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_single_type_name_lists(p):
    '''single_type_name_lists : single_type_name_lists single_type_name_list
                              | single_type_name_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]


def p_name_list(p):
    '''name_list : name_list ID
                 | ID'''
    if len(p) == 2:
        p[0] = [Name(p[1])]
    else:
        p[1].append(Name(p[2]))
        p[0] = p[1]


def p_single_type_name_list(p):
    '''single_type_name_list : name_list DASH type'''
    result = []
    for name in p[1]:
        new_name = Name(name.name)
        new_name.type = p[3]
        result.append(new_name)
    p[0] = result


def p_type(p):
    '''type : ID'''
    p[0] = p[1]


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


def p_predicate_def(p):
    '''predicate_def : unparametrised_predicate_def
                     | parametrised_predicate_def'''
    p[0] = p[1]


def p_unparametrised_predicate_def(p):
    '''unparametrised_predicate_def : LPAREN ID RPAREN'''
    predicate_name = p[2]
    new_predicate = Predicate(predicate_name)
    p[0] = new_predicate


def p_parametrised_predicate_def(p):
    '''parametrised_predicate_def : LPAREN ID typed_variable_list RPAREN'''
    predicate_name = p[2]
    new_predicate = Predicate(predicate_name)
    new_predicate.variables = p[3]
    p[0] = new_predicate


# If we have any typed names, they must come first.
def p_typed_variable_list(p):
    '''typed_variable_list : variable_list
                           | single_type_variable_lists
                           | single_type_variable_lists variable_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_single_type_variable_lists(p):
    '''single_type_variable_lists : single_type_variable_lists single_type_variable_list
                                  | single_type_variable_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[1].extend(p[2])
        p[0] = p[1]


def p_single_type_variable_list(p):
    '''single_type_variable_list : variable_list DASH ID'''
    result = []
    for variable in p[1]:
        new_name = Variable(variable.name)
        new_name.type = p[3]
        result.append(new_name)
    p[0] = result


def p_variable_list(p):
    '''variable_list : variable_list PARAMETER
                     | PARAMETER'''
    if len(p) == 2:
        variable = Variable(p[1])
        if variable.name in type_of:
            variable.type = type_of[variable.name]
        p[0] = [variable]
    else:
        variable = Variable(p[2])
        if variable.name in type_of:
            variable.type = type_of[variable.name]
        p[1].append(variable)
        p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

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

