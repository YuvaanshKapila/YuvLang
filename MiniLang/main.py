# main.py

# Assuming the Interpreter and ASTNode classes are in the same directory
# or already imported from another module.

class ASTNode:
    def __init__(self, node_type, value=None, left=None, right=None, children=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right
        self.children = children if children else []

# Main code to test the Interpreter class
def main():
    # Create an instance of the Interpreter class
    interpreter = Interpreter()

    # Test: Variable assignment
    print("Testing Variable Assignment:")
    var_assign_node = ASTNode("ASSIGN", left=ASTNode("ID", value="x"), right=ASTNode("NUMBER", value="10"))
    interpreter.evaluate(var_assign_node)  # Assign x = 10
    print(f"Value of x: {interpreter.variables['x']}")  # Should output 10.0

    # Test: Simple arithmetic operations
    print("\nTesting Arithmetic Operations:")
    add_node = ASTNode("ADD", left=ASTNode("NUMBER", value="5"), right=ASTNode("NUMBER", value="3"))
    result = interpreter.evaluate(add_node)
    print(f"5 + 3 = {result}")  # Should output 8.0

    sub_node = ASTNode("SUB", left=ASTNode("NUMBER", value="10"), right=ASTNode("NUMBER", value="4"))
    result = interpreter.evaluate(sub_node)
    print(f"10 - 4 = {result}")  # Should output 6.0

    # Test: Function definition and calling
    print("\nTesting Function Definition and Call:")
    # Define function: square(x) { return x * x; }
    func_node = ASTNode("FUNC_DEF", value="square", children=["x", [
        ASTNode("RETURN", children=[ASTNode("MUL", left=ASTNode("ID", value="x"), right=ASTNode("ID", value="x"))])
    ]])

    # Define a function call: square(5)
    func_call_node = ASTNode("FUNC_CALL", value="square", children=[ASTNode("NUMBER", value="5")])

    # Define the function
    interpreter.evaluate(func_node)

    # Call the function and get the result
    result = interpreter.evaluate(func_call_node)
    print(f"square(5) = {result}")  # Should output 25.0

    # Test: Conditional (IF) statement
    print("\nTesting IF statement:")
    if_node = ASTNode("IF", children=[
        ASTNode("BOOLEAN", value=True),  # Condition: True
        ASTNode("ASSIGN", left=ASTNode("ID", value="y"), right=ASTNode("NUMBER", value="100")),
        ASTNode("ASSIGN", left=ASTNode("ID", value="y"), right=ASTNode("NUMBER", value="200"))
    ])
    interpreter.evaluate(if_node)
    print(f"Value of y (if condition True): {interpreter.variables['y']}")  # Should output 100.0

    # Test: Array handling
    print("\nTesting Array Handling:")
    array_node = ASTNode("ARRAY", children=[
        ASTNode("NUMBER", value="1"),
        ASTNode("NUMBER", value="2"),
        ASTNode("NUMBER", value="3")
    ])
    result = interpreter.evaluate(array_node)
    print(f"Array [1, 2, 3]: {result}")  # Should output [1.0, 2.0, 3.0]

if __name__ == "__main__":
    main()
