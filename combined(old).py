
#1 - only output 

# import ply.lex as lex
# import ply.yacc as yacc

# # List of token names - defines the types of tokens the lexer will recognize
# tokens = (
#     'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
#     'IDENTIFIER', 'ASSIGN', 'LBRACKET', 'RBRACKET', 'COMMA',
#     'FOR', 'WHILE', 'IN', 'RANGE', 'COLON',
#     'IF', 'ELSE', 'EQUALS', 'LT', 'GT'
# )

# # Regular expression rules for simple tokens - these define token patterns for single-character tokens
# t_PLUS = r'\+'
# t_MINUS = r'-'
# t_TIMES = r'\*'
# t_DIVIDE = r'/'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_ASSIGN = r'='
# t_LBRACKET = r'\['
# t_RBRACKET = r'\]'
# t_COMMA = r','
# t_COLON = r':'
# t_EQUALS = r'=='
# t_LT = r'<'
# t_GT = r'>'

# # Token rule to handle numbers - identifies numeric values and converts them to integers
# def t_NUMBER(t):
#     r'\d+'
#     t.value = int(t.value)
#     return t

# # Token rule for identifiers (variable names) and keywords - checks for special keywords (e.g., 'for', 'while')
# def t_IDENTIFIER(t):
#     r'[a-zA-Z_][a-zA-Z0-9_]*'
#     if t.value == 'for':
#         t.type = 'FOR'
#     elif t.value == 'while':
#         t.type = 'WHILE'
#     elif t.value == 'in':
#         t.type = 'IN'
#     elif t.value == 'range':
#         t.type = 'RANGE'
#     elif t.value == 'if':
#         t.type = 'IF'
#     elif t.value == 'else':
#         t.type = 'ELSE'
#     return t

# # Ignored characters (whitespace and tabs)
# t_ignore = ' \t'

# # Error handling rule for lexer - prints an error message for unrecognized characters and skips them
# error_flag = False  # Global error flag

# def t_error(t):
#     global error_flag
#     print(f"Illegal character '{t.value[0]}'")
#     t.lexer.skip(1)
#     error_flag = True

# # Build the lexer - transforms the token definitions above into a lexer object
# #Lexer is a component of a compiler or interpreter that processes input text and converts it into a sequence of tokens
# lexer = lex.lex() 

# # Parsing rules - define grammar for the language and actions to take when patterns match

# # Rule to parse different types of statements
# def p_statement(p):
#     '''statement : arithmetic_expr
#                  | array_declaration
#                  | loop
#                  | if_statement
#                  | simple_declaration'''
#     p[0] = p[1]

# # Parsing rule for arithmetic expressions with addition and subtraction
# def p_arithmetic_expr(p):
#     '''arithmetic_expr : arithmetic_expr PLUS term
#                        | arithmetic_expr MINUS term
#                        | term'''
#     if len(p) == 4:
#         if p[2] == '+':
#             p[0] = p[1] + p[3]
#         elif p[2] == '-':
#             p[0] = p[1] - p[3]
#     else:
#         p[0] = p[1]

# # Parsing rule for terms in arithmetic expressions - handles multiplication and division
# def p_term(p):
#     '''term : term TIMES factor
#             | term DIVIDE factor
#             | factor'''
#     if len(p) == 4:
#         if p[2] == '*':
#             p[0] = p[1] * p[3]
#         elif p[2] == '/':
#             p[0] = p[1] / p[3]
#     else:
#         p[0] = p[1]

# # Parsing rule for factors - handles numbers and expressions in parentheses
# def p_factor(p):
#     '''factor : NUMBER
#               | LPAREN arithmetic_expr RPAREN'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = p[2]

# # Parsing rule for array declarations
# def p_array_declaration(p):
#     'array_declaration : IDENTIFIER ASSIGN LBRACKET item_list RBRACKET'
#     p[0] = f"Array '{p[1]}' initialized with items {p[4]}"

# # Parsing rule for lists within array declarations
# def p_item_list(p):
#     '''item_list : NUMBER
#                  | NUMBER COMMA item_list
#                  | '''
#     if len(p) == 1:
#         p[0] = []
#     elif len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = [p[1]] + p[3]

# # Parsing rule for different types of loops
# def p_loop(p):
#     '''loop : for_loop
#             | while_loop'''
#     p[0] = p[1]

# # Parsing rule for 'for' loops
# def p_for_loop(p):
#     'for_loop : FOR IDENTIFIER IN RANGE LPAREN NUMBER COMMA NUMBER RPAREN COLON suite'
#     p[0] = f"For loop iterating from {p[6]} to {p[8]} with iterator '{p[2]}': {p[11]}"

# # Parsing rule for 'while' loops
# def p_while_loop(p):
#     'while_loop : WHILE condition COLON suite'
#     p[0] = f"While loop with condition '{p[2]}': {p[4]}"

# # Parsing rule for if-else statements
# def p_if_statement(p):
#     'if_statement : IF condition COLON suite ELSE COLON suite'
#     p[0] = f"If statement with condition '{p[2]}': {p[4]}, else: {p[7]}"

# # Parsing rule for conditions (comparison expressions)
# def p_condition(p):
#     '''condition : IDENTIFIER EQUALS NUMBER
#                  | IDENTIFIER LT NUMBER
#                  | IDENTIFIER GT NUMBER'''
#     p[0] = f"{p[1]} {p[2]} {p[3]}"

# # Parsing rule for a suite (sequence of statements)
# def p_suite(p):
#     'suite : IDENTIFIER ASSIGN NUMBER'
#     p[0] = f"{p[1]} = {p[3]}"

# # Parsing rule for simple variable assignment statements
# def p_simple_declaration(p):
#     'simple_declaration : IDENTIFIER ASSIGN NUMBER'
#     p[0] = f"Variable '{p[1]}' assigned value {p[3]}"

# # Error handling rule for parser - triggered when syntax error is detected
# def p_error(p):
#     global error_flag
#     if p:
#         print(f"Syntax error at '{p.value}'")
#     else:
#         print("Syntax error at EOF")
#     error_flag = True

# # Build the parser - uses parsing rules defined above to generate a parser object
# #parser is a crucial component in your code that
# #allows you to analyze and process input data according to the grammar rules you've defined using the PLY library.
# parser = yacc.yacc()

# # Function to parse input and print results or errors
# def parse_and_print(input_string):
#     global error_flag
#     error_flag = False  # Reset error flag for each new input
#     result = parser.parse(input_string, lexer=lexer)
    
#     if not error_flag:
#         print(f"Input: {input_string}")
#         print(f"Output: {result}\n")
#     else:
#         print(f"Input: {input_string}")
#         print("Output: Syntax error encountered.\n")

# # Interactive menu function to allow user to select different types of constructs to parse
# def menu():
#     while True:
#         print("Select an option:")
#         print("1. Arithmetic Expression")
#         print("2. Array Declaration")
#         print("3. For Loop")
#         print("4. While Loop")
#         print("5. If Statement")
#         print("6. Simple Declaration")
#         print("7. Exit")
        
#         choice = input("Enter choice: ")
        
#         if choice == '1':
#             input_string = input("Enter arithmetic expression: ")
#             parse_and_print(input_string)
#         elif choice == '2':
#             input_string = input("Enter array declaration: ")
#             parse_and_print(input_string)
#         elif choice == '3':
#             input_string = input("Enter for loop: ")
#             parse_and_print(input_string)
#         elif choice == '4':
#             input_string = input("Enter while loop: ")
#             parse_and_print(input_string)
#         elif choice == '5':
#             input_string = input("Enter if statement: ")
#             parse_and_print(input_string)
#         elif choice == '6':
#             input_string = input("Enter simple declaration: ")
#             parse_and_print(input_string)
#         elif choice == '7':
#             break
#         else:
#             print("Invalid choice. Please try again.")

# # Run the interactive menu
# menu()

#2 - output + AST but no GUI

import ply.lex as lex
import ply.yacc as yacc
import sys

# -----------------------------------------------------------------------------
# AST (Abstract Syntax Tree) Node Definitions
# -----------------------------------------------------------------------------

class Node:
    """Base class for all AST nodes."""
    def __repr__(self):
        return f"{self.__class__.__name__}"

class BinOpNode(Node):
    """Represents a binary operation (e.g., 5 + x)."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumberNode(Node):
    """Represents a numeric literal (int or float)."""
    def __init__(self, value):
        self.value = value

class VariableNode(Node):
    """Represents an identifier/variable."""
    def __init__(self, name):
        self.name = name

class AssignmentNode(Node):
    """Represents an assignment (e.g., x = 10)."""
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ListNode(Node):
    """Represents a list declaration (e.g., [1, x, 3])."""
    def __init__(self, items):
        self.items = items

class IfNode(Node):
    """Represents an if/else statement."""
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class ForNode(Node):
    """Represents a for loop."""
    def __init__(self, iterator, start, end, body):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.body = body

class WhileNode(Node):
    """Represents a while loop."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

# -----------------------------------------------------------------------------
# Lexer
# -----------------------------------------------------------------------------

tokens = (
    # Literals and Identifiers
    'NUMBER', 'IDENTIFIER',
    # Operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    # Delimiters
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'COLON',
    # Keywords
    'FOR', 'WHILE', 'IN', 'RANGE', 'IF', 'ELSE',
    # Comparison Operators
    'EQUALS', 'NE', 'LT', 'GT', 'LE', 'GE',
)

# Regular expressions for simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_COLON     = r':'
t_ASSIGN    = r'='
t_EQUALS    = r'=='
t_NE        = r'!='
t_LE        = r'<='
t_GE        = r'>='
t_LT        = r'<'
t_GT        = r'>'

t_ignore = ' \t'

keywords = {
    'for': 'FOR', 'while': 'WHILE', 'in': 'IN', 'range': 'RANGE',
    'if': 'IF', 'else': 'ELSE'
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_statement(p):
    """
    statement : assignment
              | expression
              | if_statement
              | for_loop
              | while_loop
    """
    p[0] = p[1]

def p_assignment(p):
    """
    assignment : IDENTIFIER ASSIGN expression
               | IDENTIFIER ASSIGN list_literal
    """
    p[0] = AssignmentNode(VariableNode(p[1]), p[3])

def p_list_literal(p):
    """
    list_literal : LBRACKET item_list RBRACKET
    """
    p[0] = ListNode(p[2])

def p_item_list(p):
    """
    item_list : expression
              | item_list COMMA expression
              |
    """
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_if_statement(p):
    """
    if_statement : IF condition COLON statement ELSE COLON statement
                 | IF condition COLON statement
    """
    if len(p) == 8:
        p[0] = IfNode(p[2], p[4], p[7])
    else:
        p[0] = IfNode(p[2], p[4])

def p_for_loop(p):
    """
    for_loop : FOR IDENTIFIER IN RANGE LPAREN expression COMMA expression RPAREN COLON statement
    """
    p[0] = ForNode(VariableNode(p[2]), p[6], p[8], p[11])

def p_while_loop(p):
    """
    while_loop : WHILE condition COLON statement
    """
    p[0] = WhileNode(p[2], p[4])

def p_condition(p):
    """
    condition : expression comparison_op expression
    """
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_comparison_op(p):
    """
    comparison_op : EQUALS
                  | NE
                  | LT
                  | GT
                  | LE
                  | GE
    """
    p[0] = p[1]

def p_expression(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    """
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression_factor(p):
    """
    expression : factor
    """
    p[0] = p[1]

def p_factor(p):
    """
    factor : NUMBER
           | IDENTIFIER
           | LPAREN expression RPAREN
    """
    if len(p) == 2:
        if isinstance(p[1], (int, float)):
            p[0] = NumberNode(p[1])
        else:
            p[0] = VariableNode(p[1])
    else:
        p[0] = p[2]

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, token='{p.value}' (type='{p.type}')")
    else:
        print("Syntax error at end of file")
    parser.error = True

parser = yacc.yacc()
parser.error = False

# -----------------------------------------------------------------------------
# AST Pretty Printer
# -----------------------------------------------------------------------------

def print_ast(node, indent=0):
    if node is None:
        return

    prefix = "  " * indent
    if isinstance(node, (NumberNode, VariableNode)):
        print(f"{prefix}{node.__class__.__name__}({node.value if isinstance(node, NumberNode) else node.name})")
    elif isinstance(node, BinOpNode):
        print(f"{prefix}BinOp(op='{node.op}')")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, AssignmentNode):
        print(f"{prefix}Assignment:")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, ListNode):
        print(f"{prefix}List:")
        for item in node.items:
            print_ast(item, indent + 1)
    elif isinstance(node, IfNode):
        print(f"{prefix}If:")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Body:")
        print_ast(node.if_body, indent + 2)
        if node.else_body:
            print(f"{prefix}  Else:")
            print_ast(node.else_body, indent + 2)
    elif isinstance(node, ForNode):
        print(f"{prefix}For:")
        print(f"{prefix}  Iterator: {node.iterator.name}")
        print(f"{prefix}  Range Start:")
        print_ast(node.start, indent + 2)
        print(f"{prefix}  Range End:")
        print_ast(node.end, indent + 2)
        print(f"{prefix}  Body:")
        print_ast(node.body, indent + 2)
    elif isinstance(node, WhileNode):
        print(f"{prefix}While:")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Body:")
        print_ast(node.body, indent + 2)
    else:
        print(f"{prefix}Unknown Node: {node}")

# -----------------------------------------------------------------------------
# Main Execution Logic
# -----------------------------------------------------------------------------


def validate_syntax(input_string, choice):
    """Validates syntax based on the selected option"""
    try:
        if choice == '1':  # Arithmetic Expression
            if not any(op in input_string for op in ['+', '-', '*', '/']):
                return False, "Invalid arithmetic expression. Must contain operators (+,-,*,/)"
        elif choice == '2':  # List Declaration
            if not ('=' in input_string and '[' in input_string and ']' in input_string):
                return False, "Invalid list declaration. Format: name = [items]"
        elif choice == '3':  # For Loop
            if not all(x in input_string for x in ['for', 'in', 'range', ':', '(']):
                return False, "Invalid for loop. Format: for var in range(start, end): statement"
        elif choice == '4':  # While Loop
            if not all(x in input_string for x in ['while', ':']):
                return False, "Invalid while loop. Format: while condition: statement"
        elif choice == '5':  # If Statement
            if not ('if' in input_string and ':' in input_string):
                return False, "Invalid if statement. Format: if condition: statement [else: statement]"
        elif choice == '6':  # Assignment
            if '=' not in input_string:
                return False, "Invalid assignment. Format: variable = value"
        return True, "Syntax valid"
    except:
        return False, "Invalid syntax"

def evaluate_expression(node, variables=None):
    """Evaluates the AST nodes to produce actual output"""
    if variables is None:
        variables = {}
    
    if isinstance(node, NumberNode):
        return node.value
    elif isinstance(node, VariableNode):
        return variables.get(node.name, 0)  # Default to 0 if variable not found
    elif isinstance(node, BinOpNode):
        left = evaluate_expression(node.left, variables)
        right = evaluate_expression(node.right, variables)
        
        if node.op == '+': return left + right
        elif node.op == '-': return left - right
        elif node.op == '*': return left * right
        elif node.op == '/': return left / right if right != 0 else float('inf')
        elif node.op in ['==', '!=', '<', '>', '<=', '>=']:
            ops = {
                '==': lambda x, y: x == y,
                '!=': lambda x, y: x != y,
                '<': lambda x, y: x < y,
                '>': lambda x, y: x > y,
                '<=': lambda x, y: x <= y,
                '>=': lambda x, y: x >= y
            }
            return ops[node.op](left, right)
    elif isinstance(node, ListNode):
        return [evaluate_expression(item, variables) for item in node.items]
    elif isinstance(node, AssignmentNode):
        value = evaluate_expression(node.right, variables)
        variables[node.left.name] = value
        return value
    return None

def parse_and_print_ast(input_string, choice='7'):
    """
    Parses a single line of code, prints the AST if successful,
    and evaluates the expression if possible.
    """
    # First validate syntax
    is_valid, message = validate_syntax(input_string, choice)
    if not is_valid:
        print(f"\nSyntax Error: {message}")
        return

    parser.error = False
    ast = parser.parse(input_string, lexer=lexer)

    print("\n" + "="*20 + " RESULT " + "="*20)
    print(f"Input: {input_string}\n")

    if not parser.error and ast:
        print("--- Abstract Syntax Tree (AST) ---")
        print_ast(ast)
        
        # Add evaluation result
        result = evaluate_expression(ast)
        if result is not None:
            print("\n--- Evaluation Result ---")
            print(f"Output: {result}")
            print(f"Type: {type(result).__name__}")
    else:
        print("--- Output ---\nFailed to parse due to syntax errors.")
    
    print("="*48 + "\n")

def menu():
    """
    Presents an interactive menu to the user for parsing different code constructs.
    """
    variables = {}  # Store variables for evaluation context
    
    while True:
        print("Enhanced PLY Parser - Select an option:")
        print("1. Arithmetic Expression (e.g., 3 + 5 * 2)")
        print("2. List Declaration (e.g., myList = [1, 2, 3])")
        print("3. For Loop (e.g., for i in range(1, 5): x = 10)")
        print("4. While Loop (e.g., while x < 5: y = 20)")
        print("5. If Statement (e.g., if x == 5: y = 10 else: y = 20)")
        print("6. Simple Assignment (e.g., x = 42)")
        print("7. General Statement (Try anything that correlates with above 6!)")
        print("8. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '8':
            print("Exiting.")
            break
        
        if choice not in ['1', '2', '3', '4', '5', '6', '7']:
            print("Invalid choice. Please try again.\n")
            continue
            
        prompts = {
            '1': "Enter arithmetic expression: ",
            '2': "Enter list declaration: ",
            '3': "Enter for loop: ",
            '4': "Enter while loop: ",
            '5': "Enter if statement: ",
            '6': "Enter simple assignment: ",
            '7': "Enter any statement: "
        }
        
        input_string = input(prompts[choice])
        parse_and_print_ast(input_string, choice)

if __name__ == "__main__":
    menu()