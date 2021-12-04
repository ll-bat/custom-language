from compiler.parser import Parser
from compiler.interpreter import Interpreter
from utils.errors import *
from compiler.semantic_analyzer import SemanticAnalyzer

try:
    string = """
        PROGRAM Part10;
            VAR
               number     : INTEGER;
               a, b, c, x : INTEGER;
               y          : REAL;
               s          : STRING;
            
            PROCEDURE p1 (a, b : INTEGER);
            BEGIN
                s := "something";
                y := 222;
                c := a + b;
                print(c);
                print("print" + " " + s, "really", "interesting");
            END;
                        
            PROCEDURE p2;
            BEGIN
                print(y);
            END;
            
            BEGIN {Part10}
               BEGIN
                  number := 2;
                  a := number;
                  b := 10 * a + 10 * number DIV 4;
                  c := a - - b;
                  p1 (1 + 2, 3);
               END;
                              
               p2();
               
               x := 11;               
               y := 20 / 7 + 3.14;
               
               p2();
               
               { writeln('a = ', a); }
               { writeln('b = ', b); }
               { writeln('c = ', c); }
               { writeln('number = ', number); }
               { writeln('x = ', x); }
               { writeln('y = ', y); }
            END.  {Part10}
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

