# Interpreter Documentation

## **Overview**

The `Interpreter` class is a basic interpreter for evaluating arithmetic expressions, handling control flow structures (like `if` and `while` loops), defining and calling functions, and managing variables. It supports operations like addition, subtraction, multiplication, division, and more, as well as user-defined functions.

## **Class: `Interpreter`**

The `Interpreter` class is the main class used to evaluate abstract syntax tree (AST) nodes and execute various operations in the language.

### **Initialization**

```python
class Interpreter:
    def __init__(self):
        self.variables = {}  # Holds variable names and values
        self.functions = {}  # Holds function definitions
variables: A dictionary that stores the variables and their respective values.
functions: A dictionary that stores function definitions by name.
Methods
evaluate(node)
Evaluates an AST node based on its type and performs the corresponding operation.

python
Copy code
def evaluate(self, node):
    # Handle different node types (e.g., number, variable, operations)
Parameters:
node: An instance of ASTNode, which represents the current operation or value to be evaluated.
Returns: The result of the evaluation, which could be a number, string, or boolean.
execute_block(block)
Executes a block of statements. This method is used in control structures like if statements, while loops, or function bodies.

python
Copy code
def execute_block(self, block):
    # Executes a series of statements in a block
Parameters:
block: A list of ASTNode objects, representing the block of code to be executed.
Returns: None.
ASTNode Class
The ASTNode class is used to represent a single node in the abstract syntax tree. Each node can represent an operation, a value, or a variable.

Initialization
python
Copy code
class ASTNode:
    def __init__(self, node_type, value=None, left=None, right=None, children=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right
        self.children = children if children else []
node_type: The type of the node, e.g., "NUMBER", "ID", "ADD", "FUNC_DEF", etc.
value: The value of the node (e.g., number, string, variable name).
left, right: Left and right children of the node (used for binary operations).
children: A list of child nodes (used for control structures or function definitions).
Usage
Example 1: Variable Assignment
python
Copy code
var_assign_node = ASTNode("ASSIGN", left=ASTNode("ID", value="x"), right=ASTNode("NUMBER", value="10"))
interpreter.evaluate(var_assign_node)
This example assigns the value 10 to the variable x.
You can access the variable using interpreter.variables["x"].
Example 2: Arithmetic Operations
python
Copy code
add_node = ASTNode("ADD", left=ASTNode("NUMBER", value="5"), right=ASTNode("NUMBER", value="3"))
result = interpreter.evaluate(add_node)
print(result)  # Outputs: 8.0
This evaluates 5 + 3 and outputs the result 8.0.
Example 3: Function Definition and Call
python
Copy code
# Define function: square(x) { return x * x; }
func_node = ASTNode("FUNC_DEF", value="square", children=["x", [
    ASTNode("RETURN", children=[ASTNode("MUL", left=ASTNode("ID", value="x"), right=ASTNode("ID", value="x"))])
]])

# Call function: square(5)
func_call_node = ASTNode("FUNC_CALL", value="square", children=[ASTNode("NUMBER", value="5")])

# Define the function and call it
interpreter.evaluate(func_node)
result = interpreter.evaluate(func_call_node)
print(result)  # Outputs: 25.0
This defines a square function and calls it with the argument 5, returning 25.0.
Example 4: Conditional Statement
python
Copy code
if_node = ASTNode("IF", children=[
    ASTNode("BOOLEAN", value=True),  # Condition: True
    ASTNode("ASSIGN", left=ASTNode("ID", value="y"), right=ASTNode("NUMBER", value="100")),
    ASTNode("ASSIGN", left=ASTNode("ID", value="y"), right=ASTNode("NUMBER", value="200"))
])
interpreter.evaluate(if_node)
print(interpreter.variables["y"])  # Outputs: 100.0
This evaluates an IF statement where the condition is True. The variable y will be assigned the value 100.
Example 5: While Loop
python
Copy code
while_node = ASTNode("WHILE", children=[
    ASTNode("GT", left=ASTNode("ID", value="x"), right=ASTNode("NUMBER", value="0")),
    ASTNode("ASSIGN", left=ASTNode("ID", value="x"), right=ASTNode("SUB", left=ASTNode("ID", value="x"), right=ASTNode("NUMBER", value="1")))
])
interpreter.evaluate(while_node)
print(interpreter.variables["x"])  # Will print the value of x after the loop completes
This evaluates a while loop that runs as long as x > 0 and decrements x by 1 in each iteration.
Error Handling
If an unknown node type is encountered during evaluation, the evaluate method raises an exception:

python
Copy code
raise ValueError(f"Unknown node type: {node.type}")
Future Extensions
The interpreter currently supports basic operations, variable assignments, conditional logic, loops, and function calls. Future improvements could include:

Support for more complex data types like arrays or objects.
Improved error handling for undefined variables or invalid operations.
Optimization for repeated expressions and functions.
Advanced features like scoping rules for variables and functions, recursion, and more complex built-in functions.
Conclusion
This interpreter is a simple but extensible starting point for evaluating an abstract syntax tree (AST) and can be customized for more complex language features. You can define variables, perform operations, create functions, and use control structures like if and while loops in the interpreter.
