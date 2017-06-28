"""
Tokenizer for a PDDL domain and problem files.
"""
import ply.lex as lex

reserved = {
    'define': 'DEFINE',
    'domain': 'DOMAIN',
    ':requirements': 'REQUIREMENTS',
    ':constants': 'CONSTANTS',
    ':strips': 'STRIPS',
    ':equality': 'EQUALITY',
    ':typing': 'TYPING',
    ':adl': 'ADL',
    ':predicates': 'PREDICATES',
    ':action': 'ACTION',
    ':parameters': 'PARAMETERS',
    ':precondition': 'PRECONDITION',
    ':effect': 'EFFECT',
    'forall': 'FORALL',
    'exists': 'EXISTS',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'when': 'WHEN',
    'problem': 'PROBLEM',
    ':domain': 'DOMAIN_DEF',
    ':objects': 'OBJECTS',
    ':init': 'INIT',
    ':goal': 'GOAL',
    ':types': 'TYPES',
}

tokens = ['ID', 'DASH', 'LPAREN', 'RPAREN', 'EQUALS', 'COMMENT', 'DEF', 'PARAMETER'] + list(reserved.values())

# Regular expression rules for simple tokens
t_DASH   = r'\-'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS  = r'\='
t_ignore_COMMENT = r'\;.*'


def t_ID(t):
    r'[a-zA-Z_-][a-zA-Z_0-9-]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_DEF(t):
    r'\:?[a-zA-Z][a-zA-Z]*'
    value = t.value.lower()
    if value in reserved:
        t.type = reserved[value]
    return t


def t_PARAMETER(t):
    r'\?[a-zA-Z0-9]+'
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


def main():
    import sys

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        # Remove single line comments
        data = f.read()

    lexer.input(data)

    for tok in lexer:
        print(tok)

if __name__ == '__main__':
    main()


