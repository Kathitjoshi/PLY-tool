# 🚀 Enhanced PLY Parser & Interpreter

**A comprehensive lexer, parser, and interpreter built with Python using PLY (Python Lex-Yacc) and Tkinter GUI.**

![Language](https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![Parser](https://img.shields.io/badge/Parser-PLY-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

## ✨ Features

### 🔤 **Complete Lexical Analysis**
- **Token Recognition**: Numbers, strings, identifiers, operators, keywords
- **Keyword Support**: `for`, `while`, `if`, `else`, `print`, `True`, `False`, `range`
- **Operator Support**: Arithmetic (`+`, `-`, `*`, `/`) and comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- **Error Handling**: Comprehensive lexical error detection and reporting

### 🌳 **Abstract Syntax Tree (AST) Generation**
- **Node Types**: Variables, literals, binary operations, assignments, control structures
- **Visual AST Display**: Hierarchical tree representation with proper indentation
- **Complete Coverage**: Support for all language constructs

### 🔄 **Full Interpreter Implementation**
- **Variable Management**: Global symbol table with dynamic typing
- **Control Flow**: If/else statements, for loops, while loops
- **Built-in Functions**: `str()` function with extensible architecture
- **Data Types**: Numbers, booleans, strings, lists
- **Runtime Error Handling**: Division by zero, undefined variables, type errors

### 🎨 **Modern GUI Interface**
- **Code Editor**: Syntax-highlighted input with scroll support
- **Live Output**: Real-time AST visualization and program execution
- **Error Display**: Detailed error messages with line numbers
- **Clean Layout**: Professional themed interface using TTK widgets

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- PLY (Python Lex-Yacc) library

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kathitjoshi/PLY-tool.git
   cd PLY-tool
   ```

2. **Install Dependencies**
   ```bash
   pip install ply
   ```
   > **Note:** Tkinter comes pre-installed with most Python distributions.

3. **Run the Application**
   ```bash
   python combined.py
   ```

## 💻 Language Support

### Supported Syntax

#### **Variables & Data Types**
```python
x = 10                    # Integer
name = "Hello World"      # String  
flag = True               # Boolean
my_list = [1, 2, "text"]  # List
```

#### **Control Structures**
```python
# If/Else Statements
if x > 5: 
    print("Greater than 5") 
else: 
    print("Less than or equal to 5")

# For Loops
for i in range(0, 10): 
    print(i)

# While Loops  
while x > 0: 
    print(x)
    x = x - 1
```

#### **Built-in Functions**
```python
print("Hello World")      # Output function
str(42)                   # Type conversion
```

### Example Program
```python
x = 10
if x > 5: print("x is greater than 5") else: print("x is not greater than 5")
for i in range(0, 3): print(i)
while x > 8: print("x is " + str(x)); x = x - 1
my_list = [1, "hello", True]
print(my_list)
```

## 🏗️ Architecture


### Core Components

#### **AST Node Classes**
- `Node`: Base class for all AST nodes
- `BlockNode`: Sequence of statements
- `BinOpNode`: Binary operations (`+`, `-`, `==`, etc.)
- `NumberNode`, `StringNode`, `BooleanNode`: Literal values
- `VariableNode`: Identifier references
- `AssignmentNode`: Variable assignments
- `IfNode`, `ForNode`, `WhileNode`: Control flow
- `PrintNode`: Output statements
- `FunctionCallNode`: Function invocations

#### **Lexer (Tokenizer)**
- Regular expression-based token recognition
- Keyword vs identifier disambiguation
- Line number tracking for error reporting

#### **Parser (Syntax Analyzer)**
- Context-free grammar implementation
- Operator precedence handling
- Error recovery and reporting

#### **Interpreter (Evaluator)**
- Tree-walking interpreter
- Dynamic variable binding
- Built-in function registry

## 🎯 Use Cases

### 🎓 **Educational Applications**
- **Compiler Theory**: Learn lexing, parsing, and interpretation
- **Language Design**: Experiment with syntax and semantics
- **Algorithm Visualization**: See how parsers build ASTs

### 🛠️ **Development Tools**
- **DSL Prototyping**: Quick domain-specific language testing
- **Code Analysis**: Understanding parser implementation
- **Academic Projects**: Comprehensive compiler construction example

## 🔧 Technical Details

- **Language**: Python 3.7+
- **Parser Generator**: PLY (Python Lex-Yacc)
- **GUI Framework**: Tkinter with TTK themes
- **Architecture Pattern**: Visitor pattern for AST traversal
- **Error Handling**: Multi-stage error reporting (lexical, syntactic, semantic)

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Extended Language Features**
  - [ ] Function definitions and calls
  - [ ] Dictionary data type
  - [ ] List comprehensions
  - [ ] Exception handling

- [ ] **IDE Features**
  - [ ] Syntax highlighting in editor
  - [ ] Line numbers and debugging
  - [ ] File import/export
  - [ ] Code completion

- [ ] **Advanced Parsing**
  - [ ] Better error recovery
  - [ ] Symbol table management
  - [ ] Type checking system

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings for new classes and methods
- Include test cases for new features
- Update documentation as needed

## 📝 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/Kathitjoshi)
- Project Link: [PLY Parser & Interpreter](https://github.com/Kathitjoshi/PLY-tool)

## 🙏 Acknowledgments

- **PLY (Python Lex-Yacc)** - Powerful parsing tools for Python
- **Python Community** - For excellent documentation and resources
- **Compiler Design Principles** - Inspiration from classic textbooks

---

<div align="center">

**Built with ❤️ using Python, PLY, and Tkinter**

⭐ **Star this repo if you found it helpful!** ⭐


</div>
