from typing import List

from compiler.lexer import Lexer
from utils.constants import *
from utils.data_classes import *
from utils.errors import ParserError, ErrorCode


class Parser:
    """
    --------- GRAMMAR ---------------
    program: PROGRAM variable block
    block:  LCBRACE declarations compound_statement RCBRACE
    declarations:
        VAR (variable_declaration SEMI)+
        | FUNCTION ID (LPARENT formal_parameter_list RPARENT)? block
        | empty
    formal_parameter_list: formal_parameter (SEMI format_parameter)*
    format_parameter: ID (COMMA ID)* COLON integer_type
    variable_declaration: ID (COMMA, ID)* COLON base_type
    base_type: INTEGER | REAL | STRING | BOOLEAN
    compound_statement: statement_list
    statement_list: statement (SEMI statement)*
    statement: assignment_statement | function_call | declarations | empty
    function_call: ID LPARENT (base_expr (COMMA base_expr)*)* RPARENT SEMI
    empty:
    assignment_statement: variable ASSIGN base_expr
    base_expr: expr | str_expr | bool_expr
    bool_expr: bool_term ((OR, AND) bool_term)*
    bool_term: NOT bool_term | LPARENT bool_expr RPARENT | TRUE | FALSE
    str_expr: STRING (PLUS (STRING|variable))*
    expr: term ((PLUS, MINUS) term)*
    term: factor ((DIV, MULT, FLOAT_DIV) factor)*
    factor: PLUS factor | MINUS factor | INTEGER | REAL_INTEGER | LPARENT expr RPARENT | variable | function_call
    variable: ID
    """

    def __init__(self, text):
        self.lexer = Lexer(text)

    def print_surrounding_tokens(self):
        print("surrounding tokens")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        for i in range(5):
            if self.lexer.get_current_token().type is not EOF:
                print(self.lexer.get_current_token())
                self.lexer.go_forward()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def is_function_call(self):
        return self.next_tokens_are(ID, LPARENT)

    def is_assignment(self):
        return self.next_tokens_are(ID, ASSIGN)

    def is_declaration(self):
        token = self.lexer.get_current_token()
        return token.type in (VAR, FUNCTION)

    def next_tokens_are(self, *args):
        self.lexer.save_current_state()
        state = True
        for arg in args:
            token = self.lexer.get_current_token()
            if token.type is not arg:
                state = False
                break
            self.lexer.go_forward()

        self.lexer.use_saved_state()
        return state

    def program(self):
        self.match(PROGRAM)
        self.variable()
        block = self.block()
        return Program(block)

    def block(self):
        self.match(LCBRACE)
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        self.match(RCBRACE)
        return Block(declarations, compound_statement)

    def function_block(self):
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def function_return_statement(self):
        returns = None
        if self.next_tokens_are(RETURN):
            self.match(RETURN)
            returns = self.base_expr()
        return returns

    def declarations(self) -> list:
        declarations = []

        while self.lexer.get_current_token().type in (VAR, FUNCTION):
            if self.lexer.get_current_token().type is VAR:
                self.match(VAR)
                while self.next_tokens_are(ID, COMMA) or self.next_tokens_are(ID, COLON):
                    # var x, y || var x : integer
                    declarations.append(self.variable_declaration())
                    self.match(SEMI)

            while self.lexer.get_current_token().type is FUNCTION:
                self.match(FUNCTION)
                proc_name = self.lexer.get_current_token().value
                self.match(ID)

                parameters_list = []
                if self.lexer.current_token.type is LPARENT:
                    self.match(LPARENT)
                    parameters_list = self.parameters_list()
                    self.match(RPARENT)

                self.match(LCBRACE)
                block = self.function_block()
                returns = self.function_return_statement()
                self.match(SEMI)
                self.match(RCBRACE)

                function_decl = FunctionDecl(proc_name, parameters_list, block, returns)
                declarations.append(function_decl)

        return declarations

    def parameters_list(self) -> list:
        """
        ( a , b : INTEGER; c : REAL ) or ()
        """

        declarations = []

        if self.lexer.get_current_token().type is RPARENT:
            return declarations

        var = self.lexer.get_current_token().value
        declarations.append(var)
        self.match(ID)

        while self.lexer.get_current_token().type is COMMA:
            self.match(COMMA)
            var = self.lexer.get_current_token().value
            declarations.append(var)
            self.match(ID)

        self.match(COLON)
        base_type = self.base_type()
        declarations = list(map(lambda x: VarSymbol(x, base_type.value), declarations))

        if self.lexer.get_current_token().type is not RPARENT:
            self.match(SEMI)
            declarations.extend(self.parameters_list())

        return declarations

    def variable_declaration(self):
        variables = []
        if self.lexer.get_current_token().type is not ID:
            self.error('should be ID, got: ' + self.lexer.get_current_token().type)

        variables.append(self.lexer.get_current_token())
        self.lexer.go_forward()

        while self.lexer.get_current_token().type is COMMA:
            self.lexer.go_forward()
            var = self.lexer.get_current_token()
            if var.type is not ID:
                self.error('should be ID, got: ' + self.lexer.get_current_token().type)
            variables.append(var)
            self.lexer.go_forward()

        self.match(COLON)
        base_type = self.base_type()
        return VarDecs(variables, base_type)

    def base_type(self):
        token = self.lexer.get_current_token()
        if token.type in (INTEGER, REAL, STRING, BOOLEAN):
            self.lexer.go_forward()
            return token

        self.error('should be integer|real|string|boolean, got ' + token.type)

    def integer_type(self):
        token = self.lexer.get_current_token()
        if token.type in (INTEGER, REAL):
            self.lexer.go_forward()
            return token

        self.error('should be integer|real, got ' + token.type)

    def compound_statement(self):
        nodes = self.statement_list()
        compound = Compound()
        for node in nodes:
            compound.add(node)

        return compound

    def is_compound_statement(self):
        return self.is_function_call() or self.is_assignment() or self.is_declaration()

    def statement_list(self):
        children = []
        statement = self.statement()
        if isinstance(statement, list):
            for node in statement:
                children.append(node)
        else:
            children.append(statement)

        while self.is_compound_statement():
            statement = self.statement_list()
            if isinstance(statement, list):
                for node in statement:
                    children.append(node)
            else:
                children.append(statement)

        return children

    def statement(self):
        token = self.lexer.get_current_token()

        if self.is_function_call():
            # function call
            node = self.function_call()
            self.match(SEMI)
            return node
        elif self.is_assignment():
            # assignment
            node = self.assignment_statement()
            self.match(SEMI)
            return node
        elif self.is_declaration():
            # variable or function declaration
            return self.declarations()
        elif token.type in (RCBRACE, RETURN):
            # compound_statement finished here
            # we use a trick here
            # just return an emtpy token
            return self.emtpy()

        self.error("should be ID or LPARENT, got {}".format(token))

    def function_call(self):
        """
        function_call: ID LPARENT (base_expr (COMMA base_expr)*)* RPARENT
        """
        current_token = self.lexer.get_current_token()
        proc_name = self.lexer.get_current_token().value
        self.match(ID)
        self.match(LPARENT)
        if self.lexer.get_current_token().type is RPARENT:
            self.match(RPARENT)
            # no parameters
            return FunctionCall(proc_name, [], current_token)
        else:
            params = [self.base_expr()]
            while self.lexer.get_current_token().type is COMMA:
                self.match(COMMA)
                params.append(self.base_expr())
            self.match(RPARENT)
            return FunctionCall(proc_name, params, current_token)

    def assignment_statement(self):
        var = self.variable()
        self.match(ASSIGN)
        base_expr = self.base_expr()
        return Assign(var, Token(ASSIGN, Assign), base_expr)

    def base_expr(self):
        token = self.lexer.get_current_token()
        if token.type is STRING:
            return self.str_expr()
        elif self.next_tokens_are(NOT) or self.next_tokens_are(BOOLEAN):
            return self.bool_expr()
        else:
            return self.expr()

    def bool_expr(self):
        #  bool_expr: bool_term ((OR, AND) bool_term)*
        bool_term = self.bool_term()
        while self.lexer.get_current_token().type in (OR, AND):
            op = self.lexer.get_current_token()
            self.lexer.go_forward()
            bool_term = BoolOp(bool_term, op, self.bool_term())

        return bool_term

    def bool_term(self):
        #  bool_term: NOT bool_term | LPARENT bool_expr RPARENT | TRUE | FALSE
        token = self.lexer.get_current_token()
        if token.type is NOT:
            self.match(NOT)
            return NotOp(self.bool_term())

        if token.type is BOOLEAN:
            self.match(BOOLEAN)
            return BooleanSymbol(token.value)

        if token.type is LPARENT:
            self.match(LPARENT)
            node = self.bool_expr()
            self.match(RPARENT)
            return node

        self.error("error in bool_term, got {}".format(token))

    def str_expr(self):
        var = self.lexer.current_token
        if var.type is STRING:
            var = Str(var)
        elif var.type is ID:
            var = Var(var)
        else:
            self.error("string assignment can only contain string literals")

        self.lexer.go_forward()
        while self.lexer.get_current_token().type is PLUS:
            self.match(PLUS)
            var = StrOp(var, Token(PLUS, PLUS), self.str_expr())

        return var

    @staticmethod
    def emtpy():
        return NoOp()

    def variable(self):
        token = self.lexer.get_current_token()
        if token.type is ID:
            self.lexer.go_forward()
            return Var(token)

        self.error("error in variable")

    def error(self, message, error_code=None):
        self.print_surrounding_tokens()

        if error_code is None:
            error_code = ErrorCode.PARSER_ERROR
        raise ParserError(
            error_code=error_code,
            message=f'{error_code.value} -> {message}',
        )

    def match(self, token_type: str):
        token = self.lexer.get_current_token()
        if token.type is not token_type:
            print('-----------------------')
            print(token)
            print('should be: ' + token_type)
            print('-----------------------')
            self.error("incorrect expression")
        self.lexer.go_forward()

    def expr(self):
        node = self.term()
        while self.lexer.get_current_token().type in (PLUS, MINUS):
            current_op_token = self.lexer.get_current_token()
            self.lexer.go_forward()
            node = BinOp(node, current_op_token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.lexer.get_current_token().type in (MULT, FLOAT_DIV, INTEGER_DIV):
            current_op_token = self.lexer.get_current_token()
            self.lexer.go_forward()
            node = BinOp(node, current_op_token, self.factor())
        return node

    def factor(self):
        token = self.lexer.get_current_token()
        if token.type is PLUS:
            self.match(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type is MINUS:
            self.match(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.lexer.go_forward()
            return Num(token)
        elif token.type == FLOAT:
            self.lexer.go_forward()
            return Num(token)
        elif token.type is LPARENT:
            self.match(LPARENT)
            node = self.expr()
            self.match(RPARENT)
            return node
        elif self.is_function_call():
            return self.function_call()
        elif token.type is ID:
            self.lexer.go_forward()
            return Var(token)
        else:
            self.error("incorrect expression: (from factor)")

    def parse(self):
        program = self.program()

        if self.lexer.is_pointer_out_of_text():
            # all characters consumed
            return program

        self.error("Syntax error at position " + str(self.lexer.get_position()))
