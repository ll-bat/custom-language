import abc


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'


class NodeVisitor(object):
    def visit(self, node):
        class_name = type(node).__name__
        method_name = 'visit_' + class_name
        method = getattr(self, method_name)
        return method(node)


class AST:
    pass


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Num({self.token.type}, {self.value})'


class Str(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Str({self.value})'


class StrOp(AST):
    def __init__(self, left, add: Token, right):
        self.left = left
        self.add = add
        self.right = right

    def __str__(self):
        return f'StrOp({self.left}, {self.add}, {self.right})'


class BinOp(AST):
    def __init__(self, left, op: Token, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'BinOp({self.left}, {self.op.type}, {self.right})'


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return f'UnaryOp({self.op}, {self.expr})'


class Compound(AST):
    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children

    def __str__(self):
        res = ""
        for node in self.children:
            res += str(node) + ", "

        return f'Compound({res})'


class Var(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Var({self.value})'


class Assign(AST):
    def __init__(self, left: Var, op: Token, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f'Assign({self.left}, :=, {self.right})'


class NoOp(AST):
    def __str__(self):
        return 'NoOp()'


class VarDecs(AST):
    def __init__(self, variables, base_type: Token):
        self.variables = variables
        self.token = self.type = base_type

    def get_declarations(self):
        return self.variables

    def get_type(self) -> Token:
        return self.type

    def __str__(self):
        res = ""
        for var in self.variables:
            res += var.value + ', '
        return f'VarDecs(({res}), {self.type.value})'


class Program(AST):
    def __init__(self, block):
        self.block = block

    def __str__(self):
        return f'Program({self.block})'


class Block(AST):
    def __init__(self, var_decs: list, compound_statement: Compound):
        self.var_decs = var_decs
        self.compound_statement = compound_statement

    def __str__(self):
        res = ""
        for dec in self.var_decs:
            res += str(dec) + ", "
        return f'Program({res}, {self.compound_statement})'


class AbstractSymbol(abc.ABC):
    def __init__(self, name, *args):
        self.name = name

    def is_symbol(self):
        return isinstance(self, Symbol)

    def is_procedure(self):
        return isinstance(self, ProcedureDecl)


class ProcedureDecl(AbstractSymbol):
    def __init__(self, proc_name, params, block):
        super(ProcedureDecl, self).__init__(proc_name)
        self.name = proc_name
        self.block = block
        self.params = params if params is not None else []

    def __str__(self):
        return f'ProcedureDecl({self.name}, {self.params}, {self.block})'


class ProcedureCall(AST):
    def __init__(self, name, actual_params, token):
        self.name = name
        self.actual_params = actual_params
        self.token = token

    def __str__(self):
        res = ""
        for param in self.actual_params:
            res += str(param) + ", "
        return f'ProcedureCall({self.name}, {res}, {self.token})'


class Symbol(AbstractSymbol):
    def __init__(self, name, value=None):
        super().__init__(name)
        self.name = name
        self.value = value

    def __str__(self):
        return f'Symbol({self.name}, {self.value})'

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, value):
        super().__init__(name, value)


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
