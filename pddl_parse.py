import ply.yacc as yacc

# Get the token map from the lexer. Required.
from pddl_lex import tokens




# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

domain = '''
(define (domain blocks_world)
  (:requirements :strips)
  (:predicates (on-table ?x) (on ?x ?y) (clear ?x))

  (:action MoveToTable
    :parameters (?x ?y)
    :precondition (and (clear ?x) (on ?x ?y))
    :effect (and (clear ?y) (on-table ?x) (not (on ?x ?y))))

  (:action MoveToBlock1
    :parameters (?x ?y ?z)
    :precondition (and (clear ?x) (clear ?z) (on ?x ?y))
    :effect (and (clear ?y) (on ?x ?z) (not (clear ?z)) (not (on ?x ?y))))

  (:action MoveToBlock2
    :parameters (?x ?y)
    :precondition (and (clear ?x) (clear ?y) (on-table ?x))
    :effect (and (on ?x ?y) (not (clear ?y)) (not (on-table ?x))))
  )
'''

result = parser.parse(domain)
print(result)

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
