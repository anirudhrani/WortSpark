from antlr4 import InputStream, CommonTokenStream
from grammar.wandelscriptLexer import wandelscriptLexer 
from grammar.wandelscriptParser import wandelscriptParser 
from antlr4.error.ErrorListener import ErrorListener

# Custom error listener to capture syntax errors
class MyErrorListener(ErrorListener):
    def __init__(self):
        super(MyErrorListener, self).__init__()
        self.has_error = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.has_error = True

def is_valid_code(code: str) -> bool:
    # Create an input stream from the code string
    input_stream = InputStream(code)
    
    # Instantiate the lexer with the input stream
    lexer = wandelscriptLexer(input_stream)
    
    # Generate tokens from the lexer
    token_stream = CommonTokenStream(lexer)
    
    # Instantiate the parser with the token stream
    parser = wandelscriptParser(token_stream)
    
    # Remove default error listeners and add custom listener
    parser.removeErrorListeners()
    error_listener = MyErrorListener()
    parser.addErrorListener(error_listener)
    
    # Parse the input starting at the correct rule ('program')
    parser.program()  
    return not error_listener.has_error

# # a trailing newline is a must
# if __name__ == "__main__":
#     code_snippet = """a1 = 0 and 0\n"""
#     print(is_valid_code(code_snippet))  