import ply.lex as lex
import ply.yacc as yacc

# List of token names - defines the types of tokens the lexer will recognize
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'IDENTIFIER', 'ASSIGN', 'LBRACKET', 'RBRACKET', 'COMMA',
    'FOR', 'WHILE', 'IN', 'RANGE', 'COLON',
    'IF', 'ELSE', 'EQUALS', 'LT', 'GT'
)

# Regular expression rules for simple tokens - these define token patterns for single-character tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_COLON = r':'
t_EQUALS = r'=='
t_LT = r'<'
t_GT = r'>'

# Token rule to handle numbers - identifies numeric values and converts them to integers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Token rule for identifiers (variable names) and keywords - checks for special keywords (e.g., 'for', 'while')
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == 'for':
        t.type = 'FOR'
    elif t.value == 'while':
        t.type = 'WHILE'
    elif t.value == 'in':
        t.type = 'IN'
    elif t.value == 'range':
        t.type = 'RANGE'
    elif t.value == 'if':
        t.type = 'IF'
    elif t.value == 'else':
        t.type = 'ELSE'
    return t

# Ignored characters (whitespace and tabs)
t_ignore = ' \t'

# Error handling rule for lexer - prints an error message for unrecognized characters and skips them
error_flag = False  # Global error flag

def t_error(t):
    global error_flag
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
    error_flag = True

# Build the lexer - transforms the token definitions above into a lexer object
#Lexer is a component of a compiler or interpreter that processes input text and converts it into a sequence of tokens
lexer = lex.lex() 

# Parsing rules - define grammar for the language and actions to take when patterns match

# Rule to parse different types of statements
def p_statement(p):
    '''statement : arithmetic_expr
                 | array_declaration
                 | loop
                 | if_statement
                 | simple_declaration'''
    p[0] = p[1]

# Parsing rule for arithmetic expressions with addition and subtraction
def p_arithmetic_expr(p):
    '''arithmetic_expr : arithmetic_expr PLUS term
                       | arithmetic_expr MINUS term
                       | term'''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
    else:
        p[0] = p[1]

# Parsing rule for terms in arithmetic expressions - handles multiplication and division
def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
    else:
        p[0] = p[1]

# Parsing rule for factors - handles numbers and expressions in parentheses
def p_factor(p):
    '''factor : NUMBER
              | LPAREN arithmetic_expr RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Parsing rule for array declarations
def p_array_declaration(p):
    'array_declaration : IDENTIFIER ASSIGN LBRACKET item_list RBRACKET'
    p[0] = f"Array '{p[1]}' initialized with items {p[4]}"

# Parsing rule for lists within array declarations
def p_item_list(p):
    '''item_list : NUMBER
                 | NUMBER COMMA item_list
                 | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Parsing rule for different types of loops
def p_loop(p):
    '''loop : for_loop
            | while_loop'''
    p[0] = p[1]

# Parsing rule for 'for' loops
def p_for_loop(p):
    'for_loop : FOR IDENTIFIER IN RANGE LPAREN NUMBER COMMA NUMBER RPAREN COLON suite'
    p[0] = f"For loop iterating from {p[6]} to {p[8]} with iterator '{p[2]}': {p[11]}"

# Parsing rule for 'while' loops
def p_while_loop(p):
    'while_loop : WHILE condition COLON suite'
    p[0] = f"While loop with condition '{p[2]}': {p[4]}"

# Parsing rule for if-else statements
def p_if_statement(p):
    'if_statement : IF condition COLON suite ELSE COLON suite'
    p[0] = f"If statement with condition '{p[2]}': {p[4]}, else: {p[7]}"

# Parsing rule for conditions (comparison expressions)
def p_condition(p):
    '''condition : IDENTIFIER EQUALS NUMBER
                 | IDENTIFIER LT NUMBER
                 | IDENTIFIER GT NUMBER'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"

# Parsing rule for a suite (sequence of statements)
def p_suite(p):
    'suite : IDENTIFIER ASSIGN NUMBER'
    p[0] = f"{p[1]} = {p[3]}"

# Parsing rule for simple variable assignment statements
def p_simple_declaration(p):
    'simple_declaration : IDENTIFIER ASSIGN NUMBER'
    p[0] = f"Variable '{p[1]}' assigned value {p[3]}"

# Error handling rule for parser - triggered when syntax error is detected
def p_error(p):
    global error_flag
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")
    error_flag = True

# Build the parser - uses parsing rules defined above to generate a parser object
#parser is a crucial component in your code that
#allows you to analyze and process input data according to the grammar rules you've defined using the PLY library.
parser = yacc.yacc()

# Function to parse input and print results or errors
def parse_and_print(input_string):
    global error_flag
    error_flag = False  # Reset error flag for each new input
    result = parser.parse(input_string, lexer=lexer)
    
    if not error_flag:
        print(f"Input: {input_string}")
        print(f"Output: {result}\n")
    else:
        print(f"Input: {input_string}")
        print("Output: Syntax error encountered.\n")

# Interactive menu function to allow user to select different types of constructs to parse
def menu():
    while True:
        print("Select an option:")
        print("1. Arithmetic Expression")
        print("2. Array Declaration")
        print("3. For Loop")
        print("4. While Loop")
        print("5. If Statement")
        print("6. Simple Declaration")
        print("7. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            input_string = input("Enter arithmetic expression: ")
            parse_and_print(input_string)
        elif choice == '2':
            input_string = input("Enter array declaration: ")
            parse_and_print(input_string)
        elif choice == '3':
            input_string = input("Enter for loop: ")
            parse_and_print(input_string)
        elif choice == '4':
            input_string = input("Enter while loop: ")
            parse_and_print(input_string)
        elif choice == '5':
            input_string = input("Enter if statement: ")
            parse_and_print(input_string)
        elif choice == '6':
            input_string = input("Enter simple declaration: ")
            parse_and_print(input_string)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

# Run the interactive menu
menu()
