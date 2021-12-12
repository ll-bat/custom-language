from compiler.parser import Parser
from compiler.interpreter import Interpreter
from utils.errors import *
from compiler.semantic_analyzer import SemanticAnalyzer
try:
    string = """
        PROGRAM Part10
        {
            var sum : integer; 
            var cnt : integer; 
            sum = 0;
            cnt = 0;
            
            for i = 0; i < 1000; i = i + 1 {
            }   
            
        }  
    """

    # lexer = Lexer(string)
    # while lexer.get_current_token().type is not EOF:
    #     print(lexer.get_current_token())
    #     lexer.go_forward()

    parser = Parser(string)
    tree = parser.parse()
    # print(tree)

    # check for errors
    semantic_analyzer = SemanticAnalyzer(tree)
    semantic_analyzer.analyze()

    # interpret language
    interpreter = Interpreter(tree)
    interpreter.interpret()
    print(interpreter.get_recursion_count())
except (ParserError, SemanticError, LexerError) as ex:
    print(ex)
except Exception as e:
    print(e)
