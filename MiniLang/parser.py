class ASTNode:
    def __init__(self, type_, value=None, left=None, right=None, children=None):
        self.type = type_
        self.value = value
        self.left = left
        self.right = right
        self.children = children if children else []

    def __repr__(self):
        return f"{self.type}({self.value})"

# Parser class with expanded grammar
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        if len(self.tokens) > 0:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, but got {self.current_token}")

    # Grammar rule for expressions (including logical and comparison operators)
    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        node = self.parse_logic_or()
        if self.current_token and self.current_token[0] == "ASSIGN":
            self.eat("ASSIGN")
            node = ASTNode("ASSIGN", left=node, right=self.parse_expression())
        return node

    def parse_logic_or(self):
        node = self.parse_logic_and()
        while self.current_token and self.current_token[0] == "OR":
            self.eat("OR")
            node = ASTNode("OR", left=node, right=self.parse_logic_and())
        return node

    def parse_logic_and(self):
        node = self.parse_comparison()
        while self.current_token and self.current_token[0] == "AND":
            self.eat("AND")
            node = ASTNode("AND", left=node, right=self.parse_comparison())
        return node

    def parse_comparison(self):
        node = self.parse_term()
        while self.current_token and self.current_token[0] in ("EQ", "NEQ", "LT", "LEQ", "GT", "GEQ"):
            token = self.current_token
            if token[0] == "EQ":
                self.eat("EQ")
                node = ASTNode("EQ", left=node, right=self.parse_term())
            elif token[0] == "NEQ":
                self.eat("NEQ")
                node = ASTNode("NEQ", left=node, right=self.parse_term())
            elif token[0] == "LT":
                self.eat("LT")
                node = ASTNode("LT", left=node, right=self.parse_term())
            elif token[0] == "LEQ":
                self.eat("LEQ")
                node = ASTNode("LEQ", left=node, right=self.parse_term())
            elif token[0] == "GT":
                self.eat("GT")
                node = ASTNode("GT", left=node, right=self.parse_term())
            elif token[0] == "GEQ":
                self.eat("GEQ")
                node = ASTNode("GEQ", left=node, right=self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token and self.current_token[0] in ("PLUS", "MINUS"):
            token = self.current_token
            if token[0] == "PLUS":
                self.eat("PLUS")
                node = ASTNode("ADD", value="+", left=node, right=self.parse_factor())
            elif token[0] == "MINUS":
                self.eat("MINUS")
                node = ASTNode("SUB", value="-", left=node, right=self.parse_factor())
        return node

    def parse_factor(self):
        node = self.parse_primary()
        while self.current_token and self.current_token[0] in ("TIMES", "DIVIDE", "MOD", "POWER"):
            token = self.current_token
            if token[0] == "TIMES":
                self.eat("TIMES")
                node = ASTNode("MUL", value="*", left=node, right=self.parse_primary())
            elif token[0] == "DIVIDE":
                self.eat("DIVIDE")
                node = ASTNode("DIV", value="/", left=node, right=self.parse_primary())
            elif token[0] == "MOD":
                self.eat("MOD")
                node = ASTNode("MOD", value="%", left=node, right=self.parse_primary())
            elif token[0] == "POWER":
                self.eat("POWER")
                node = ASTNode("POWER", value="^", left=node, right=self.parse_primary())
        return node

    def parse_primary(self):
        token = self.current_token
        if token[0] == "NUMBER":
            self.eat("NUMBER")
            return ASTNode("NUMBER", value=token[1])
        elif token[0] == "STRING":
            self.eat("STRING")
            return ASTNode("STRING", value=token[1][1:-1])  # Remove the quotes
        elif token[0] == "TRUE":
            self.eat("TRUE")
            return ASTNode("BOOLEAN", value=True)
        elif token[0] == "FALSE":
            self.eat("FALSE")
            return ASTNode("BOOLEAN", value=False)
        elif token[0] == "ID":
            self.eat("ID")
            return ASTNode("ID", value=token[1])
        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_expression()
            self.eat("RPAREN")
            return node
        elif token[0] == "LBRACKET":
            self.eat("LBRACKET")
            elements = []
            while self.current_token and self.current_token[0] != "RBRACKET":
                elements.append(self.parse_expression())
                if self.current_token and self.current_token[0] == "COMMA":
                    self.eat("COMMA")
            self.eat("RBRACKET")
            return ASTNode("ARRAY", children=elements)
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    # Parsing block statements (e.g., if, while)
    def parse_block(self):
        statements = []
        while self.current_token and self.current_token[0] != "RBRACE":
            statements.append(self.parse_statement())
        return statements

    # Parsing a full statement
    def parse_statement(self):
        if self.current_token[0] == "IF":
            return self.parse_if()
        elif self.current_token[0] == "WHILE":
            return self.parse_while()
        elif self.current_token[0] == "FOR":
            return self.parse_for()
        elif self.current_token[0] == "DEF":
            return self.parse_function_def()
        elif self.current_token[0] == "RETURN":
            return self.parse_return()
        else:
            return self.parse_expression()

    # Parsing an if statement
    def parse_if(self):
        self.eat("IF")
        self.eat("LPAREN")
        condition = self.parse_expression()
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = self.parse_block()
        self.eat("RBRACE")
        else_body = None
        if self.current_token and self.current_token[0] == "ELSE":
            self.eat("ELSE")
            self.eat("LBRACE")
            else_body = self.parse_block()
            self.eat("RBRACE")
        return ASTNode("IF", children=[condition, body, else_body])

    # Parsing a while loop
    def parse_while(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        condition = self.parse_expression()
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = self.parse_block()
        self.eat("RBRACE")
        return ASTNode("WHILE", children=[condition, body])

    # Parsing a for loop
    def parse_for(self):
        self.eat("FOR")
        self.eat("LPAREN")
        init = self.parse_expression()  # Initialization
        self.eat("SEMI")
        condition = self.parse_expression()  # Condition
        self.eat("SEMI")
        update = self.parse_expression()  # Update
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = self.parse_block()  # Body of loop
        self.eat("RBRACE")
        return ASTNode("FOR", children=[init, condition, update, body])

    # Parsing function definition
    def parse_function_def(self):
        self.eat("DEF")
        name = self.current_token[1]  # Function name
        self.eat("ID")
        self.eat("LPAREN")
        params = []
        while self.current_token and self.current_token[0] == "ID":
            params.append(self.current_token[1])
            self.eat("ID")
            if self.current_token and self.current_token[0] == "COMMA":
                self.eat("COMMA")
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = self.parse_block()
        self.eat("RBRACE")
        return ASTNode("FUNC_DEF", value=name, children=params + [body])

    # Parsing return statement
    def parse_return(self):
        self.eat("RETURN")
        return ASTNode("RETURN", children=[self.parse_expression()])
