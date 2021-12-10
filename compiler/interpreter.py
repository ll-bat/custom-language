from typing import List
from utils.errors import InterpreterError, ErrorCode
from system.builtin_functions.main import *
from compiler.scopes import NestedScopeable
from compiler.symbol_table import SymbolTable
from utils.data_classes import *
from utils.constants import *


class Interpreter(NodeVisitor, NestedScopeable):
    def __init__(self, tree):
        self.tree = tree
        super().__init__(SymbolTable())

    def error(self, message):
        raise InterpreterError(ErrorCode.INTERPRETER_ERROR, message)

    def visit_BinOp(self, node: BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = node.token.type

        types = {
            PLUS: lambda x, y: x + y,
            MINUS: lambda x, y: x - y,
            MULT: lambda x, y: x * y,
            INTEGER_DIV: lambda x, y: x // y,
            FLOAT_DIV: lambda x, y: x / y,
        }

        return types[operator](left, right)

    def visit_UnaryOp(self, node: UnaryOp):
        op: Token = node.op
        expr = node.expr
        if op.type is PLUS:
            return +self.visit(expr)
        else:
            return -self.visit(expr)

    @staticmethod
    def visit_Num(node: Num):
        return node.value

    @staticmethod
    def visit_Str(node: Str):
        return node.value

    def visit_StrOp(self, node: StrOp):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if type(left) is not str or type(right) is not str:
            self.error("can only concatenate string and string")

        return left + right

    def visit_Compound(self, node: Compound):
        for sub_node in node.get_children():
            self.visit(sub_node)

    def visit_Assign(self, node: Assign):
        var_name = node.left.value
        expr = self.visit(node.right)

        if self.symbol_table.is_defined(var_name):
            # type checking
            symbol: Symbol = self.symbol_table.lookup(var_name)
            base_type = symbol.type
            if not is_val_of_type(expr, base_type):
                self.error(
                    "can't assign {} to var {} as type of {} is {}".format(expr, symbol.name, symbol.name, base_type))
            return self.symbol_table.assign(var_name, Symbol(var_name, expr, base_type))
        else:
            raise ValueError(f"value {var_name} is not defined")

    def visit_Var(self, node: Var):
        var_name = node.value

        # type: Symbol
        symbol = self.symbol_table.lookup(var_name)
        if symbol is None:
            raise SyntaxError("variable '" + var_name + "' is not defined")

        if isinstance(symbol, FunctionDecl):
            return symbol

        return symbol.value

    def visit_NoOp(self, node):
        pass

    def visit_Program(self, node: Program):
        nested_symbol_table = SymbolTable(enclosed_parent=None)
        self.symbol_table = nested_symbol_table

        self.visit(node.block)

        self.symbol_table = self.symbol_table.enclosed_parent

    def visit_Block(self, node: Block):
        for declaration in node.var_decs:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecs(self, node: VarDecs):
        declarations = node.get_declarations()
        symbol_type = node.get_type()
        # print(symbol_type)
        for var in declarations:
            symbol = VarSymbol(var.value, symbol_type.value, symbol_type.value)
            self.symbol_table.define(symbol)

    def visit_VarSymbol(self, node: VarSymbol):
        self.symbol_table.define(node)

    def visit_FunctionDecl(self, node: FunctionDecl):
        self.symbol_table.define(node)

    def visit_FunctionCall(self, node: FunctionCall):
        if self.symbol_table.is_defined(node.name) is False:
            # system function call
            if is_system_function(node.name):
                params = [self.visit(param) for param in node.actual_params]
                return call_system_function(node.name, *params)
            else:
                raise NameError("no such function: " + node.name)

        function: FunctionDecl = self.symbol_table.lookup(node.name)
        parameter_names: List[Symbol] = function.params
        parameter_values = node.actual_params
        params = {}
        for var, val in zip(parameter_names, parameter_values):
            params[var.name] = self.visit(val)

        self.define_new_scope()
        for param, item in params.items():
            self.symbol_table.define(Symbol(param, item))

        block = function.block
        self.visit(block)

        returns = self.visit(function.return_expression)
        self.destroy_current_scope()

        return returns

    @staticmethod
    def visit_BooleanSymbol(node: BooleanSymbol):
        return node.value

    # def visit_BoolOp(self, node: BoolOp):
    #     left = self.visit(node.left)
    #     op = node.op.value
    #     right = self.visit(node.right)
    #     return evaluate_bool_expression(left, op, right)

    def visit_NotOp(self, node: NotOp):
        val = self.visit(node.expr)
        return not_bool(val)

    def visit_BoolNotEqual(self, node: BoolNotEqual):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return not_equal(left, right)

    def visit_BoolOr(self, node: BoolOr):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_or(left, right)

    def visit_BoolAnd(self, node: BoolAnd):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_and(left, right)

    def visit_BoolGreaterThan(self, node: BoolGreaterThan):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_greater_than(left, right)

    def visit_BoolGreaterThanOrEqual(self, node: BoolGreaterThanOrEqual):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_greater_than_or_equal(left, right)

    def visit_BoolLessThan(self, node: BoolLessThan):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_less_than(left, right)

    def visit_BoolLessThanOrEqual(self, node: BoolLessThanOrEqual):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_less_than_or_equal(left, right)

    def visit_BoolIsEqual(self, node: BoolIsEqual):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return bool_is_equal(left, right)

    def visit_IfBlock(self, node: IfBlock):
        flag = self.visit(node.expr)
        if flag is TRUE:
            self.define_new_scope()
            self.visit(node.block)
            self.destroy_current_scope()
            return True
        return False

    def visit_IfStat(self, node: IfStat):
        for if_block in node.if_blocks:
            visited: bool = self.visit(if_block)
            if visited is True:
                return
        if node.else_block is not None:
            self.visit(node.else_block)

    @staticmethod
    def visit_NoneType(node):
        return None

    def interpret(self):
        return self.visit(self.tree)
