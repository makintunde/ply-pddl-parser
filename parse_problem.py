"""
Parser for PDDL problem files.
"""

import ply.yacc as yacc

# Get the token map from the lexer. Required.
from problem import Problem
from pddl_lex import tokens
from parse_domain import p_requirements_declr, p_requirements_def, p_requirement
from parse_domain import p_typed_name_list, p_name_list, p_single_type_name_list, p_single_type_name_lists, p_type

def p_problem(p):
    'problem_declr : LPAREN DEFINE problem_def RPAREN'
    p[0] = p[3]


def p_problem_def(p):
    '''problem_def : LPAREN PROBLEM ID RPAREN domain_declr problem_components init_declr goal_declr'''
    pddl_problem = Problem(p[3])
    pddl_problem.domain = p[5]
    pddl_problem.set_components(p[6])
    pddl_problem.init_state = p[7]
    pddl_problem.goal_state = p[8]
    p[0] = pddl_problem


def p_domain_declr(p):
    '''domain_declr : LPAREN DOMAIN_DECLR ID RPAREN'''
    p[0] = p[3]


def p_problem_components(p):
    '''problem_components : problem_components problem_component
                          | problem_component'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_problem_component(p):
    '''problem_component : requirements_declr
                         | objects_declr'''
    p[0] = p[1]


def p_objects_declr(p):
    '''objects_declr : LPAREN OBJECTS typed_name_list RPAREN'''
    p[0] = (p[2], p[3])


def p_init_declr(p):
    '''init_declr : LPAREN INIT grounded_predicates RPAREN'''
    p[0] = p[3]


def p_grounded_predicates(p):
    '''grounded_predicates : grounded_predicates grounded_predicate
                           | grounded_predicate'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_grounded_predicate(p):
    '''grounded_predicate : LPAREN atoms RPAREN'''
    p[0] = p[2]


def p_atoms(p):
    '''atoms : atoms atom
             | atom'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_atom(p):
    '''atom : ID'''
    p[0] = p[1]


def p_goal_declr(p):
    '''goal_declr : LPAREN GOAL LPAREN AND grounded_predicates RPAREN RPAREN'''
    p[0] = p[5]


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

