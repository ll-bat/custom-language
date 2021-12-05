from compiler.parser import Parser
from compiler.interpreter import Interpreter
from utils.errors import *
from compiler.semantic_analyzer import SemanticAnalyzer

try:
    string = """
        PROGRAM Part10
        {
            VAR
               number     : INTEGER;
               a, b, c, x : INTEGER;
               y          : REAL;
               s          : STRING;
            
            function p1 (a, b : INTEGER)
            {
                s = "something";
                y = 222;
                c = a + b;
                print(c);
                print("print" + " " + s, "really", "interesting");
            }
                        
            function p2()
            {
                print(y);
            }
            
            number = 2;
            a = number;
            b = 10 * a + 10 * number DIV 4;
            c = a - - b;
            
            p1 (1 + 2, 3);
                              
            {{ writeln('y = ', y); }}
            
        }  {{Part10}}
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
except (ParserError, SemanticError, LexerError) as ex:
    print(ex)
except Exception as e:
    print(e)

