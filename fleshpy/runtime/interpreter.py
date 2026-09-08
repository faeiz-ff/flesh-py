from fleshpy.error import FleshRuntimeError
from fleshpy.runtime.environment import Environment
from fleshpy.visitor import Visitor

from fleshpy import ast
from fleshpy.runtime.function import default_flesh_functions
from fleshpy.runtime.value import Function, Value, Integer, String, Boolean, \
    BuiltInFunction, Float, Nil


class Interpreter(Visitor[Value]):
    def __init__(self):
        self.env: Environment[Value] = Environment(default_flesh_functions)

    def visit_program(self, node: ast.Program) -> Value:
        for n in node.exprs[:-1]:
            n.accept(self)

        return node.exprs[-1].accept(self)

    def visit_int_literal(self, node: ast.IntLiteral) -> Value:
        return Integer(int(node.token.lexeme))

    def visit_float_literal(self, node: ast.FloatLiteral) -> Value:
        return Float(float(node.token.lexeme))

    def visit_string_literal(self, node: ast.StringLiteral) -> Value:
        return String(node.token.lexeme)

    def visit_boolean_literal(self, node: ast.BooleanLiteral) -> Value:
        return Boolean(node.token.lexeme[-1] == "t")

    def visit_definition(self, node: ast.Definition) -> Value:
        identifier = node.token.lexeme
        self.env.set(identifier, node.expr.accept(self))
        return Nil()

    def visit_identifier(self, node: ast.Identifier) -> Value:
        identifier = node.token.lexeme
        value = self.env.get(identifier)
        if value is None:
            raise FleshRuntimeError("Undefined Symbol: " + identifier)

        return value

    def visit_application(self, node: ast.Application) -> Value:
        fun = node.fun.accept(self)
        args = list(map(lambda n: n.accept(self), node.args))

        match fun:
            case BuiltInFunction(f):
                return f(args)
            case Function(lamb, env):
                if len(lamb.params) != len(args):
                    raise FleshRuntimeError(
                        "Arity mismatch, expected " +
                        str(len(lamb.params)) +
                        " got " + str(len(args))
                    )

                new_env = Environment(parent=env)

                for name, arg in zip(lamb.params, args):
                    new_env.set(name.lexeme, arg)

                temp = self.env
                self.env = new_env
                value = lamb.body.accept(self)
                self.env = temp

                return value
            case _:
                raise FleshRuntimeError("Not a function, cant be called")

    def visit_lambda(self, node: ast.Lambda) -> Value:
        # TODO: variadics
        return Function(node, self.env)

    def visit_begin(self, node: ast.Begin) -> Value:
        for n in node.expr_list[:-1]:
            n.accept(self)

        return node.expr_list[-1].accept(self)

    @staticmethod
    def is_truthy(value: Value) -> bool:
        match value:
            case Boolean(b):
                return b
            case _:
                return False

    def visit_if(self, node: ast.If) -> Value:
        cond = node.cond.accept(self)
        if Interpreter.is_truthy(cond):
            return node.then_expr.accept(self)
        else:
            return node.else_expr.accept(self)

    def visit_cond(self, node: ast.Cond) -> Value: return Nil()
    def visit_nil(self, node: ast.Nil) -> Value: return Nil()
    def visit_let(self, node: ast.Let) -> Value: return Nil()
