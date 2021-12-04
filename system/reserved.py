from utils.constants import *
from utils.data_classes import Token

RESERVED_KEYWORDS = {
    PROGRAM: Token(PROGRAM, PROGRAM),
    BEGIN: Token(BEGIN, BEGIN),
    END: Token(END, END),
    COMMA: Token(COMMA, COMMA),
    COLON: Token(COLON, COLON),
    DIV: Token(INTEGER_DIV, INTEGER_DIV),
    INTEGER: Token(INTEGER, INTEGER),
    FLOAT: Token(FLOAT, FLOAT),
    REAL: Token(REAL, REAL),
    VAR: Token(VAR, VAR),
    PROCEDURE: Token(PROCEDURE, PROCEDURE),
    STRING: Token(STRING, STRING)
}
