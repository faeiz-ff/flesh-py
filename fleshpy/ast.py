from abc import ABC, abstractmethod
from typing import List, Tuple

from fleshpy.token import Token
from fleshpy.visitor import Visitor


class AST(ABC):
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def accept[T](self, visitor: Visitor[T]) -> T: ...


class Program(AST):
    def __init__(self, exprs: List[AST]):
        self.name = "Program"
        self.exprs = exprs

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_program(self)


class IntLiteral(AST):
    def __init__(self, token: Token):
        self.name = "IntLiteral"
        self.token = token

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_int_literal(self)


class FloatLiteral(AST):
    def __init__(self, token: Token):
        self.name = "FloatLiteral"
        self.token = token

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_float_literal(self)


class StringLiteral(AST):
    def __init__(self, token: Token):
        self.name = "StringLiteral"
        self.token = token

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_string_literal(self)


class Identifier(AST):
    def __init__(self, token: Token):
        self.name = "Identifier"
        self.token = token

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_identifier(self)


class Definition(AST):
    def __init__(self, token: Token, expr: AST):
        self.name = "Definition"
        self.token = token
        self.expr = expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_definition(self)


class If(AST):
    def __init__(self, cond: AST, then_expr: AST, else_expr: AST):
        self.name = "If"
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_if(self)


class Cond(AST):
    def __init__(self, arms: List[Tuple[AST, AST]]):
        self.name = "Cond"
        self.arms = arms

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_cond(self)


class Begin(AST):
    def __init__(self, expr_list: List[AST]):
        self.name = "Begin"
        self.expr_list = expr_list

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_begin(self)


class Lambda(AST):
    def __init__(self, args: List[Token], body: AST):
        self.name = "Lambda"
        self.args = args
        self.body = body

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_lambda(self)


class Application(AST):
    def __init__(self, fun: AST, args: List[AST]):
        self.name = "Application"
        self.fun = fun
        self.args = args

    def accept[T](self, visitor: Visitor[T]) -> T:
        return visitor.visit_application(self)
