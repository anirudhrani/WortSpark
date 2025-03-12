from antlr4.error.ErrorListener import ErrorListener
from antlr4 import InputStream, CommonTokenStream
from grammar.wandelscriptLexer import wandelscriptLexer 
from grammar.wandelscriptParser import wandelscriptParser 


class WortSparkErrorListener(ErrorListener):
    def __init__(self):
        super(WortSparkErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Line {line}, Column {column}: {msg}")

def is_valid_code(code: str) -> (bool, list):
    input_stream = InputStream(code)
    lexer = wandelscriptLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = wandelscriptParser(token_stream)
    
    parser.removeErrorListeners()
    error_listener = WortSparkErrorListener()
    parser.addErrorListener(error_listener)
    
    parser.program()
    
    is_valid = len(error_listener.errors) == 0
    return is_valid, error_listener.errors

# Main
if __name__ == "__main__":
    code_snippet = """a1 = 0 and 
                    k= \n"""
    valid, errors = is_valid_code(code_snippet)
    print("Valid code:", valid)
    if not valid:
        print("Errors:")
        for err in errors:
            print(err)