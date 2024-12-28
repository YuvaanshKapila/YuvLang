class Interpreter:
    def __init__(self):
        self.variables = {}  # Holds variable names and values
        self.functions = {}  # Holds function definitions

    def evaluate(self, node):
        if node.type == "NUMBER":
            return float(node.value)
        elif node.type == "STRING":
            return node.value
        elif node.type == "BOOLEAN":
            return node.value
        elif node.type == "ID":
            return self.variables.get(node.value, None)
        elif node.type == "ADD":
            return self.evaluate(node.left) + self.evaluate(node.right)
        elif node.type == "SUB":
            return self.evaluate(node.left) - self.evaluate(node.right)
        elif node.type == "MUL":
            return self.evaluate(node.left) * self.evaluate(node.right)
        elif node.type == "DIV":
            return self.evaluate(node.left) / self.evaluate(node.right)
        elif node.type == "MOD":
            return self.evaluate(node.left) % self.evaluate(node.right)
        elif node.type == "POWER":
            return self.evaluate(node.left) ** self.evaluate(node.right)
        elif node.type == "EQ":
            return self.evaluate(node.left) == self.evaluate(node.right)
        elif node.type == "NEQ":
            return self.evaluate(node.left) != self.evaluate(node.right)
        elif node.type == "GT":
            return self.evaluate(node.left) > self.evaluate(node.right)
        elif node.type == "LT":
            return self.evaluate(node.left) < self.evaluate(node.right)
        elif node.type == "LEQ":
            return self.evaluate(node.left) <= self.evaluate(node.right)
        elif node.type == "GEQ":
            return self.evaluate(node.left) >= self.evaluate(node.right)
        elif node.type == "IF":
            condition = self.evaluate(node.children[0])
            if condition:
                return self.execute_block(node.children[1])
            elif node.children[2]:
                return self.execute_block(node.children[2])
        elif node.type == "WHILE":
            while self.evaluate(node.children[0]):
                self.execute_block(node.children[1])
        elif node.type == "FOR":
            self.evaluate(node.children[0])  # Initial action
            while self.evaluate(node.children[1]):  # Condition
                self.execute_block(node.children[3])  # Loop body
                self.evaluate(node.children[2])  # Update
        elif node.type == "FUNC_DEF":
            self.functions[node.value] = node
        elif node.type == "FUNC_CALL":
            return self.execute_function_call(node)
        elif node.type == "ASSIGN":
            return self.assign_variable(node)
        elif node.type == "ARRAY":
            return self.evaluate_array(node)
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def execute_block(self, block):
        result = None
        for stmt in block:
            result = self.evaluate(stmt)
        return result

    def assign_variable(self, node):
        # Handle assignment
        var_name = node.left.value
        value = self.evaluate(node.right)
        self.variables[var_name] = value
        return value

    def execute_function_call(self, node):
        func = self.functions.get(node.value)
        if not func:
            raise ValueError(f"Function {node.value} not defined")
        
        # Execute function call and pass arguments
        local_vars = self.variables.copy()  # Create a local environment for the function
        for param, arg in zip(func.children, node.children):
            local_vars[param] = self.evaluate(arg)
        
        # Execute the function body
        interpreter = Interpreter()
        interpreter.variables = local_vars
        result = interpreter.execute_block(func.children[-1])
        return result

    def evaluate_array(self, node):
        # Evaluate an array (returns a list of evaluated elements)
        return [self.evaluate(child) for child in node.children]
