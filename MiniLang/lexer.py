import re

# Define token types with an even broader set of symbols, keywords, and advanced constructs
TOKEN_TYPES = [
    # Basic Types and Operators
    ("NUMBER", r"\d+(\.\d*)?"),  # Integer or floating point number
    ("STRING", r'"[^"\\]*(\\.[^"\\]*)*"'),  # String literals with escape sequences
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Identifiers (variable names, function names)
    ("ASSIGN", r"="),  # Assignment operator
    ("PLUS", r"\+"),  # Plus sign
    ("MINUS", r"-"),  # Minus sign
    ("TIMES", r"\*"),  # Multiplication sign
    ("DIVIDE", r"/"),  # Division sign
    ("MOD", r"%"),  # Modulo operator
    ("POWER", r"\^"),  # Exponentiation operator
    ("INCREMENT", r"\+\+"),  # Increment operator
    ("DECREMENT", r"--"),  # Decrement operator
    ("AND", r"&&"),  # Logical AND
    ("OR", r"\|\|"),  # Logical OR
    ("NOT", r"~"),  # Logical NOT
    ("EQ", r"=="),  # Equality check
    ("NEQ", r"!="),  # Not equal check
    ("LT", r"<"),  # Less than
    ("LEQ", r"<="),  # Less than or equal
    ("GT", r">"),  # Greater than
    ("GEQ", r">="),  # Greater than or equal
    ("LPAREN", r"\("),  # Left parenthesis
    ("RPAREN", r"\)"),  # Right parenthesis
    ("LBRACE", r"\{"),  # Left brace for blocks
    ("RBRACE", r"\}"),  # Right brace for blocks
    ("LBRACKET", r"\["),  # Left bracket for arrays
    ("RBRACKET", r"\]"),  # Right bracket for arrays
    ("COLON", r":"),  # Colon (used for objects and ternary)
    ("COMMA", r","),  # Comma (used to separate arguments)
    ("SEMICOLON", r";"),  # Semicolon (end of statement)

    # Control Flow and Statements
    ("IF", r"\bif\b"),  # If keyword
    ("ELSE", r"\belse\b"),  # Else keyword
    ("WHILE", r"\bwhile\b"),  # While keyword
    ("FOR", r"\bfor\b"),  # For loop keyword
    ("SWITCH", r"\bswitch\b"),  # Switch keyword
    ("CASE", r"\bcase\b"),  # Case keyword for switch
    ("DEFAULT", r"\bdefault\b"),  # Default case in switch
    ("BREAK", r"\bbreak\b"),  # Break keyword
    ("CONTINUE", r"\bcontinue\b"),  # Continue keyword
    ("RETURN", r"\breturn\b"),  # Return keyword
    ("THROW", r"\bthrow\b"),  # Throw an exception
    ("TRY", r"\btry\b"),  # Try block for exception handling
    ("CATCH", r"\bcatch\b"),  # Catch block for exceptions
    ("FINALLY", r"\bfinally\b"),  # Finally block in exception handling
    ("YIELD", r"\byield\b"),  # Yield from a generator function

    # Object-Oriented Programming
    ("CLASS", r"\bclass\b"),  # Class keyword
    ("OBJECT", r"\{.*?\}"),  # Object literal (non-greedy)
    ("INTERFACE", r"\binterface\b"),  # Interface keyword
    ("EXTENDS", r"\bextends\b"),  # Extends keyword for class inheritance
    ("IMPLEMENTS", r"\bimplements\b"),  # Implements keyword for interfaces
    ("STATIC", r"\bstatic\b"),  # Static keyword for class members
    ("PRIVATE", r"\bprivate\b"),  # Private access modifier
    ("PUBLIC", r"\bpublic\b"),  # Public access modifier
    ("PROTECTED", r"\bprotected\b"),  # Protected access modifier
    ("CONST", r"\bconst\b"),  # Constant variable declaration
    ("VAR", r"\bvar\b"),  # Variable declaration (for dynamic typing)
    ("LET", r"\blet\b"),  # Variable declaration with block scope

    # Functional Programming
    ("LAMBDA", r"->"),  # Lambda function expression
    ("INLINE_FUNCTION", r"\binline\s+function\b"),  # Inline function declaration
    ("FUNCTION_LITERAL", r"\bfunction\s+\([^\)]*\)\s*\{[^\}]*\}"),  # Anonymous function literal
    ("TERNARY", r"\?"),  # Ternary operator
    ("TYPEOF", r"\btypeof\b"),  # Typeof operator
    ("INSTANCEOF", r"\binstanceof\b"),  # Instanceof operator for object types
    ("EVAL", r"\beval\b"),  # Eval function for runtime evaluation
    ("WITH", r"\bwith\b"),  # With statement for extending variable scope

    # Advanced Concurrency
    ("TRY_LOCK", r"\btrylock\b"),  # Try-lock for concurrency
    ("LOCK", r"\block\b"),  # Lock for concurrency
    ("UNLOCK", r"\bunlock\b"),  # Unlock for concurrency
    ("MUTEX", r"\bmutex\b"),  # Mutex for thread safety
    ("THREAD", r"\bthread\b"),  # Thread creation keyword
    ("ASYNC", r"\basync\b"),  # Async function declaration
    ("AWAIT", r"\bawait\b"),  # Await keyword in async functions
    ("DEFER", r"\bdefer\b"),  # Defer execution (for resource management)
    ("EXECUTE", r"\bexecute\b"),  # Execute command or script

    # Module and Namespace Support
    ("IMPORT", r"\bimport\b"),  # Import keyword for modules/packages
    ("EXPORT", r"\bexport\b"),  # Export keyword for modules
    ("MODULE", r"\bmodule\b"),  # Module declaration
    ("NAMESPACE", r"\bnamespace\b"),  # Namespace declaration

    # Advanced Types and Literal Expressions
    ("ARRAY_LITERAL", r"\[\s*(?:[^,\]]*\s*,\s*)*[^,\]]*\s*\]"),  # Array literal (array with elements)
    ("REGEX_LITERAL", r"\/[^\/]+\/"),  # Regular expression literal
    ("SINGLETON", r"\bsingleton\b"),  # Singleton pattern
    ("EXCEPTION", r"\bexception\b"),  # Exception type definition

    # Miscellaneous Constructs
    ("TYPE_INT", r"\bint\b"),  # Integer type
    ("TYPE_FLOAT", r"\bfloat\b"),  # Float type
    ("TYPE_STRING", r"\bstring\b"),  # String type
    ("TYPE_BOOL", r"\bbool\b"),  # Boolean type
    ("TYPE_VOID", r"\bvoid\b"),  # Void type (for function return)
    ("NULL", r"\bnull\b"),  # Null keyword
    ("TRUE", r"\btrue\b"),  # Boolean true
    ("FALSE", r"\bfalse\b"),  # Boolean false
    ("MISMATCH", r"."),  # Any other character
]

# Function to tokenize input code
def tokenize(code):
    tokens = []
    line_number = 1
    position = 0
    while position < len(code):
        match = None
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                text = match.group(0)
                if token_type != "SKIP" and token_type != "COMMENT":  # Ignore whitespaces and comments
                    tokens.append((token_type, text, line_number))
                position += len(text)
                if token_type == "NEWLINE":
                    line_number += 1
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[position]}")
    return tokens
