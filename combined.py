import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import ply.lex as lex
import ply.yacc as yacc
import sys
import io
import logging # Import the logging module

# -----------------------------------------------------------------------------
# AST (Abstract Syntax Tree) Node Definitions
# -----------------------------------------------------------------------------

class Node:
    """Base class for all AST nodes."""
    def __repr__(self):
        # Dynamically get fields for a more informative __repr__
        fields = ', '.join(f"{k}={getattr(self, k)!r}" for k in getattr(self, '_fields', []))
        return f"{self.__class__.__name__}({fields})"

class BlockNode(Node):
    """Represents a sequence of statements (e.g., body of a loop or if/else)."""
    _fields = ['statements']
    def __init__(self, statements):
        # Ensure statements is always a list
        self.statements = statements if isinstance(statements, list) else [statements]

class BinOpNode(Node):
    """Represents a binary operation (e.g., 5 + x, a == b)."""
    _fields = ['left', 'op', 'right']
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumberNode(Node):
    """Represents a numeric literal (int or float)."""
    _fields = ['value']
    def __init__(self, value):
        self.value = value

class BooleanNode(Node):
    """Represents a boolean literal (True or False)."""
    _fields = ['value']
    def __init__(self, value):
        self.value = value

class StringNode(Node):
    """Represents a string literal."""
    _fields = ['value']
    def __init__(self, value):
        # Remove quotes from the string value
        self.value = value[1:-1]

class VariableNode(Node):
    """Represents an identifier/variable."""
    _fields = ['name']
    def __init__(self, name):
        self.name = name

class AssignmentNode(Node):
    """Represents an assignment (e.g., x = 10)."""
    _fields = ['left', 'right']
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ListNode(Node):
    """Represents a list declaration (e.g., [1, x, 3])."""
    _fields = ['items']
    def __init__(self, items):
        self.items = items

class IfNode(Node):
    """Represents an if/else statement."""
    _fields = ['condition', 'if_body', 'else_body']
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class ForNode(Node):
    """Represents a for loop."""
    _fields = ['iterator', 'start', 'end', 'body']
    def __init__(self, iterator, start, end, body):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.body = body

class WhileNode(Node):
    """Represents a while loop."""
    _fields = ['condition', 'body']
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class PrintNode(Node):
    """Represents a print statement."""
    _fields = ['expr']
    def __init__(self, expr):
        self.expr = expr

class FunctionCallNode(Node):
    """Represents a function call (e.g., func(arg1, arg2))."""
    _fields = ['func_name', 'args']
    def __init__(self, func_name, args):
        self.func_name = func_name # This would be a VariableNode for the function name
        self.args = args if isinstance(args, list) else [args] # List of expression nodes

# -----------------------------------------------------------------------------
# Lexer
# -----------------------------------------------------------------------------

tokens = (
    # Literals and Identifiers
    'NUMBER', 'IDENTIFIER', 'STRING', 'TRUE', 'FALSE',
    # Operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    # Delimiters
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'COLON', 'SEMICOLON',
    # Keywords
    'FOR', 'WHILE', 'IN', 'RANGE', 'IF', 'ELSE', 'PRINT',
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
t_SEMICOLON = r';'

t_ignore = ' \t'

keywords = {
    'for': 'FOR', 'while': 'WHILE', 'in': 'IN', 'range': 'RANGE',
    'if': 'IF', 'else': 'ELSE', 'print': 'PRINT',
    'True': 'TRUE', 'False': 'FALSE'
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    if t.type in ['TRUE', 'FALSE']:
        t.value = True if t.value == 'True' else False
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    global lex_error_message
    lex_error_message = f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}"
    t.lexer.skip(1)

# Global variable to store lexer error messages
lex_error_message = None

lexer = lex.lex()

# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EQUALS', 'NE', 'LT', 'GT', 'LE', 'GE'), # Comparison operators
)

def p_program(p):
    """
    program : statement
            | program statement
    """
    if len(p) == 2:
        p[0] = BlockNode([p[1]])
    else:
        # If the first part is already a BlockNode, append to its statements
        if isinstance(p[1], BlockNode):
            p[1].statements.append(p[2])
            p[0] = p[1]
        else: # Should ideally not happen if program always returns BlockNode
            p[0] = BlockNode([p[1], p[2]])


def p_statement(p):
    """
    statement : single_statement
              | statement SEMICOLON single_statement
    """
    if len(p) == 2:
        p[0] = p[1] # Single statement
    else:
        # If p[1] is already a BlockNode, append to it
        if isinstance(p[1], BlockNode):
            p[1].statements.append(p[3])
            p[0] = p[1]
        else:
            # Otherwise, create a new BlockNode
            p[0] = BlockNode([p[1], p[3]])

def p_single_statement(p):
    """
    single_statement : assignment
                     | expression
                     | if_statement
                     | for_loop
                     | while_loop
                     | print_statement
    """
    p[0] = p[1]

def p_print_statement(p):
    """
    print_statement : PRINT LPAREN expression RPAREN
    """
    p[0] = PrintNode(p[3])

def p_assignment(p):
    """
    assignment : IDENTIFIER ASSIGN expression
               | IDENTIFIER ASSIGN list_literal
               | IDENTIFIER ASSIGN STRING
               | IDENTIFIER ASSIGN TRUE
               | IDENTIFIER ASSIGN FALSE
    """
    if p.slice[3].type == 'STRING':
        p[0] = AssignmentNode(VariableNode(p[1]), StringNode(p[3]))
    elif p.slice[3].type == 'TRUE':
        p[0] = AssignmentNode(VariableNode(p[1]), BooleanNode(True))
    elif p.slice[3].type == 'FALSE':
        p[0] = AssignmentNode(VariableNode(p[1]), BooleanNode(False))
    else:
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
           | TRUE
           | FALSE
           | STRING
           | function_call
    """
    if len(p) == 2:
        if isinstance(p[1], (int, float)):
            p[0] = NumberNode(p[1])
        elif isinstance(p[1], bool): # For TRUE/FALSE keywords
            p[0] = BooleanNode(p[1])
        elif isinstance(p[1], str) and p.slice[1].type == 'STRING': # For STRING token
            p[0] = StringNode(p[1])
        elif isinstance(p[1], Node): # Check if it's already an AST node (like FunctionCallNode)
            p[0] = p[1] # Pass it through directly
        else: # For IDENTIFIER (must be a string name for a variable)
            p[0] = VariableNode(p[1])
    else: # LPAREN expression RPAPAREN
        p[0] = p[2]

def p_function_call(p):
    """
    function_call : IDENTIFIER LPAREN arg_list RPAREN
    """
    p[0] = FunctionCallNode(VariableNode(p[1]), p[3])

def p_arg_list(p):
    """
    arg_list : expression
             | arg_list COMMA expression
             |
    """
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Global variable to store parser error messages
parser_error_message = None

def p_error(p):
    global parser_error_message
    if p:
        parser_error_message = f"Syntax error at line {p.lineno}, token='{p.value}' (type='{p.type}')"
    else:
        parser_error_message = "Syntax error at end of file"
    # Set a flag to indicate parsing error
    parser.error = True

# Explicitly provide debuglog and errorlog to ply.yacc()
# Setting debug=False is the most robust way to prevent logging issues in bundled apps.
parser = yacc.yacc(debug=False, errorlog=logging.getLogger('ply_error_logger'))
# You can still use a logger for errorlog if you want to capture errors specifically.
# The debuglog is completely suppressed by debug=False.

parser.error = False # Custom flag for parser errors

# -----------------------------------------------------------------------------
# AST Pretty Printer
# -----------------------------------------------------------------------------

def print_ast_to_string(node, indent=0):
    """Recursively prints the AST to a string."""
    output = io.StringIO()
    prefix = "  " * indent

    if node is None:
        return ""

    if isinstance(node, BlockNode):
        output.write(f"{prefix}Block:\n")
        for stmt in node.statements:
            output.write(print_ast_to_string(stmt, indent + 1))
    elif isinstance(node, (NumberNode, BooleanNode, StringNode, VariableNode)):
        value = node.value if isinstance(node, (NumberNode, BooleanNode, StringNode)) else node.name
        output.write(f"{prefix}{node.__class__.__name__}({repr(value)})\n")
    elif isinstance(node, BinOpNode):
        output.write(f"{prefix}BinOp(op='{node.op}')\n")
        output.write(print_ast_to_string(node.left, indent + 1))
        output.write(print_ast_to_string(node.right, indent + 1))
    elif isinstance(node, AssignmentNode):
        output.write(f"{prefix}Assignment:\n")
        output.write(print_ast_to_string(node.left, indent + 1))
        output.write(print_ast_to_string(node.right, indent + 1))
    elif isinstance(node, ListNode):
        output.write(f"{prefix}List:\n")
        for item in node.items:
            output.write(print_ast_to_string(item, indent + 1))
    elif isinstance(node, IfNode):
        output.write(f"{prefix}If:\n")
        output.write(f"{prefix}  Condition:\n")
        output.write(print_ast_to_string(node.condition, indent + 2))
        output.write(f"{prefix}  Body:\n")
        output.write(print_ast_to_string(node.if_body, indent + 2))
        if node.else_body:
            output.write(f"{prefix}  Else:\n")
            output.write(print_ast_to_string(node.else_body, indent + 2))
    elif isinstance(node, ForNode):
        output.write(f"{prefix}For:\n")
        output.write(f"{prefix}  Iterator: {node.iterator.name}\n")
        output.write(f"{prefix}  Range Start:\n")
        output.write(print_ast_to_string(node.start, indent + 2))
        output.write(f"{prefix}  Range End:\n")
        output.write(print_ast_to_string(node.end, indent + 2))
        output.write(f"{prefix}  Body:\n")
        output.write(print_ast_to_string(node.body, indent + 2))
    elif isinstance(node, WhileNode):
        output.write(f"{prefix}While:\n")
        output.write(f"{prefix}  Condition:\n")
        output.write(print_ast_to_string(node.condition, indent + 2))
        output.write(f"{prefix}  Body:\n")
        output.write(print_ast_to_string(node.body, indent + 2))
    elif isinstance(node, PrintNode):
        output.write(f"{prefix}Print:\n")
        output.write(print_ast_to_string(node.expr, indent + 1))
    elif isinstance(node, FunctionCallNode):
        output.write(f"{prefix}FunctionCall(name='{node.func_name.name}')\n")
        output.write(f"{prefix}  Args:\n")
        for arg in node.args:
            output.write(print_ast_to_string(arg, indent + 2))
    else:
        output.write(f"{prefix}Unknown Node: {node}\n")
    
    return output.getvalue()

# -----------------------------------------------------------------------------
# Interpreter/Evaluator
# -----------------------------------------------------------------------------

class Interpreter:
    def __init__(self):
        self.variables = {} # Global symbol table
        self.output_buffer = io.StringIO() # Buffer for print statements
        self.built_in_functions = {
            'str': self._builtin_str # Register built-in 'str' function
        }

    def _builtin_str(self, args):
        """Built-in str() function for the interpreter."""
        if not args:
            raise TypeError("str() takes at least 1 argument (0 given)")
        return str(args[0])

    def evaluate_ast(self, node):
        """Evaluates the AST nodes to produce actual output."""
        if isinstance(node, BlockNode):
            for statement in node.statements:
                self.evaluate_ast(statement) # Execute each statement in the block
            return

        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, VariableNode):
            if node.name not in self.variables:
                raise NameError(f"Name '{node.name}' is not defined.")
            return self.variables.get(node.name)
        elif isinstance(node, BinOpNode):
            left = self.evaluate_ast(node.left)
            right = self.evaluate_ast(node.right)
            
            if node.op == '+': return left + right
            elif node.op == '-': return left - right
            elif node.op == '*': return left * right
            elif node.op == '/': 
                if right == 0:
                    raise ZeroDivisionError("Division by zero.")
                return left / right
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
            return [self.evaluate_ast(item) for item in node.items]
        elif isinstance(node, AssignmentNode):
            value = self.evaluate_ast(node.right)
            self.variables[node.left.name] = value
            return value # Return the assigned value
        elif isinstance(node, IfNode):
            condition_result = self.evaluate_ast(node.condition)
            if condition_result:
                self.evaluate_ast(node.if_body)
            elif node.else_body:
                self.evaluate_ast(node.else_body)
            return
        elif isinstance(node, ForNode):
            iterator_name = node.iterator.name
            start_val = self.evaluate_ast(node.start)
            end_val = self.evaluate_ast(node.end)
            
            # Simple range simulation
            for i in range(start_val, end_val):
                self.variables[iterator_name] = i # Assign iterator value
                self.evaluate_ast(node.body)
            return
        elif isinstance(node, WhileNode):
            while self.evaluate_ast(node.condition):
                self.evaluate_ast(node.body)
            return
        elif isinstance(node, PrintNode):
            value_to_print = self.evaluate_ast(node.expr)
            self.output_buffer.write(str(value_to_print) + "\n")
            return
        elif isinstance(node, FunctionCallNode):
            func_name = node.func_name.name
            if func_name not in self.built_in_functions:
                raise NameError(f"Function '{func_name}' is not defined.")
            
            # Evaluate arguments
            evaluated_args = [self.evaluate_ast(arg) for arg in node.args]
            
            # Call the built-in function
            return self.built_in_functions[func_name](evaluated_args)
        
        # For statements that don't return a value (e.g., loops, if statements)
        return None

# -----------------------------------------------------------------------------
# Tkinter GUI Application
# -----------------------------------------------------------------------------

class ParserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced PLY Parser & Interpreter")
        self.geometry("1000x700")
        self.create_widgets()

    def create_widgets(self):
        # Configure styles
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('TFrame', background='#f0f0f0')
        s.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10, 'bold'))
        s.configure('TButton', font=('Helvetica', 10))

        # Main frame to hold everything
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Code Input", padding="10 10 10 10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.code_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=('Consolas', 10))
        self.code_input.pack(fill=tk.BOTH, expand=True)
        # Updated default code input to include str() function call
        self.code_input.insert(tk.END, 'x = 10\nif x > 5: print("x is greater than 5") else: print("x is not greater than 5")\nfor i in range(0, 3): print(i)\nwhile x > 8: print("x is " + str(x)); x = x - 1\nmy_list = [1, "hello", True]\nprint(my_list)')


        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Parse & Run", command=self.parse_and_run).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)

        # Output Sections
        # AST Output
        ast_frame = ttk.LabelFrame(main_frame, text="Abstract Syntax Tree (AST)", padding="10 10 10 10")
        ast_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.ast_output = scrolledtext.ScrolledText(ast_frame, wrap=tk.WORD, height=15, font=('Consolas', 9), state=tk.DISABLED)
        self.ast_output.pack(fill=tk.BOTH, expand=True)

        # Program Output
        program_output_frame = ttk.LabelFrame(main_frame, text="Program Output", padding="10 10 10 10")
        program_output_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.program_output = scrolledtext.ScrolledText(program_output_frame, wrap=tk.WORD, height=15, font=('Consolas', 9), state=tk.DISABLED)
        self.program_output.pack(fill=tk.BOTH, expand=True)

        # Error/Status Output
        error_frame = ttk.LabelFrame(main_frame, text="Errors / Status", padding="10 10 10 10")
        error_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        # The foreground color is set here during widget creation, not via update_text_widget
        self.error_output = scrolledtext.ScrolledText(error_frame, wrap=tk.WORD, height=5, font=('Consolas', 9), state=tk.DISABLED, foreground='red')
        self.error_output.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights to make frames expand
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=2)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def update_text_widget(self, widget, text, state='normal', append=False):
        widget.config(state=tk.NORMAL)
        if not append:
            widget.delete(1.0, tk.END)
        widget.insert(tk.END, text)
        widget.config(state=state)
        widget.see(tk.END) # Scroll to end

    def parse_and_run(self):
        # Clear previous outputs
        self.clear_outputs()
        
        code_input = self.code_input.get(1.0, tk.END).strip()
        if not code_input:
            self.update_text_widget(self.error_output, "Please enter some code to parse and run.", state=tk.DISABLED)
            return

        # Reset global error flags
        global lex_error_message, parser_error_message
        lex_error_message = None
        parser_error_message = None
        parser.error = False # Reset custom parser error flag

        try:
            # Lexing
            lexer.input(code_input)
            # You can uncomment this to see tokens in error output for debugging
            # tokens_list = []
            # while True:
            #     tok = lexer.token()
            #     if not tok: break
            #     tokens_list.append(str(tok))
            # self.update_text_widget(self.error_output, "Tokens:\n" + "\n".join(tokens_list), state=tk.DISABLED, append=True)

            if lex_error_message:
                self.update_text_widget(self.error_output, f"Lexer Error: {lex_error_message}", state=tk.DISABLED)
                return

            # Parsing
            ast_root = parser.parse(code_input, lexer=lexer)

            if parser.error or not ast_root:
                error_msg = parser_error_message if parser_error_message else "Unknown parsing error."
                self.update_text_widget(self.error_output, f"Parser Error: {error_msg}", state=tk.DISABLED)
                return

            # Display AST
            ast_string = print_ast_to_string(ast_root)
            self.update_text_widget(self.ast_output, ast_string, state=tk.DISABLED)

            # Interpret / Execute
            interpreter = Interpreter()
            try:
                interpreter.evaluate_ast(ast_root)
                program_output_text = interpreter.output_buffer.getvalue()
                if program_output_text:
                    self.update_text_widget(self.program_output, program_output_text, state=tk.DISABLED)
                else:
                    self.update_text_widget(self.program_output, "Program executed successfully. No output.", state=tk.DISABLED)
                # No 'foreground' arg here, as it's set in widget creation
                self.update_text_widget(self.error_output, "Parsing and execution successful!", state=tk.DISABLED) 

            except (NameError, TypeError, ZeroDivisionError, IndexError) as e:
                # No 'foreground' arg here
                self.update_text_widget(self.error_output, f"Runtime Error: {e}", state=tk.DISABLED)
            except Exception as e:
                # No 'foreground' arg here
                self.update_text_widget(self.error_output, f"An unexpected runtime error occurred: {e}", state=tk.DISABLED)

        except Exception as e:
            # No 'foreground' arg here
            self.update_text_widget(self.error_output, f"An unexpected error occurred during parsing: {e}", state=tk.DISABLED)

    def clear_outputs(self):
        self.update_text_widget(self.ast_output, "", state=tk.DISABLED)
        self.update_text_widget(self.program_output, "", state=tk.DISABLED)
        self.update_text_widget(self.error_output, "", state=tk.DISABLED)

    def clear_all(self):
        self.code_input.delete(1.0, tk.END)
        self.clear_outputs()


if __name__ == "__main__":
    app = ParserApp()
    app.mainloop()

