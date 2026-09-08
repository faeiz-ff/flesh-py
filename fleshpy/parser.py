
from typing import List, NoReturn, Optional, Tuple

import fleshpy.ast as ast
from fleshpy.error import FleshSyntaxError
from fleshpy.token import Token, TokenType


class Parser:
    def __init__(self):
        self.text = ""
        self.idx = 0
        self.tokens: List[Token] = []

    def curr(self) -> Optional[Token]:
        return self.tokens[self.idx] if self.idx < len(self.tokens) else None

    def check(self, ty: TokenType) -> bool:
        if self.idx < len(self.tokens):
            return self.tokens[self.idx].ty == ty

        return False

    def raiseSyntaxError(self, msg: str) -> NoReturn:
        if self.idx >= len(self.tokens):
            raise FleshSyntaxError(self.text, len(self.text) - 1, msg)
        raise FleshSyntaxError(self.text, self.tokens[self.idx].index, msg)

    def consume(self, ty: TokenType) -> None:
        if self.check(ty):
            self.idx += 1
        else:
            found_token = self.tokens[self.idx] \
                if self.idx < len(self.tokens) else self.tokens[-1]

            self.raiseSyntaxError("Expecting '" + ty.__str__() +
                                  "' but found '" + found_token.ty.__str__())

    def lambda_param(self) -> Tuple[List[Token], bool]:
        params: List[Token] = []
        variadic = False

        while not self.check(TokenType.RParen):
            tok = self.tokens[self.idx]
            if self.check(TokenType.Dot):
                self.idx += 1
                if not self.check(TokenType.ID):
                    self.raiseSyntaxError(
                        "Expecting ID after variadic declaration"
                    )
                tok = self.tokens[self.idx]
                self.idx += 1
                variadic = True
                break

            params.append(tok)
            self.consume(TokenType.ID)

        self.consume(TokenType.RParen)
        return (params, variadic)

    def define_lambda(self) -> ast.Definition:
        self.consume(TokenType.LParen)
        name = self.curr()
        if name is None:
            self.raiseSyntaxError("Name expected after 'define' keyword")
        self.idx += 1

        (params, variadic) = self.lambda_param()

        fun = ast.Lambda(params, ast.Begin(self.expression_list()), variadic)

        return ast.Definition(name, fun)

    def define(self) -> ast.Definition:
        if self.check(TokenType.LParen):
            return self.define_lambda()
        else:
            name = self.curr()
            if name is None:
                self.raiseSyntaxError("Name expected after 'define' keyword")
            self.idx += 1

            expr = self.expression()

            return ast.Definition(name, expr)

    def if_expr(self) -> ast.If:
        condition = self.expression()
        then_expr = self.expression()
        else_expr = self.expression()

        return ast.If(condition, then_expr, else_expr)

    def cond(self) -> ast.Cond:
        arms: List[Tuple[ast.AST, ast.AST]] = []

        node = ast.Cond(arms, None)  # dummy node so that i can assign

        while self.check(TokenType.LParen):
            self.consume(TokenType.LParen)

            if self.check(TokenType.Else):
                self.idx += 1
                node.else_expr = self.expression()
                break

            condition = self.expression()
            then = self.expression()

            self.consume(TokenType.RParen)

            arms.append((condition, then))

        node.arms = arms  # make sure that the arms is the recent one
        return node

    def begin(self) -> ast.Begin:
        asts = self.expression_list()
        return ast.Begin(asts)

    def lambda_expr(self) -> ast.Lambda:
        self.consume(TokenType.LParen)

        (params, variadic) = self.lambda_param()

        self.consume(TokenType.RParen)

        body = ast.Begin(self.expression_list())
        return ast.Lambda(params, body, variadic)

    def let(self) -> ast.Let:
        defs: List[Tuple[Token, ast.AST]] = []

        self.consume(TokenType.LParen)  # for defs

        while not self.check(TokenType.RParen):
            self.consume(TokenType.LParen)
            if not self.check(TokenType.ID):
                self.raiseSyntaxError("Expecting ID")

            tok = self.tokens[self.idx]
            self.consume(TokenType.ID)
            expr = self.expression()

            defs.append((tok, expr))
            self.consume(TokenType.RParen)

        self.consume(TokenType.RParen)  # for defs

        begin = self.begin()

        return ast.Let(defs, begin)

    def specials(self) -> Optional[ast.AST]:
        """Parse a special-form (without processing outside parentheses)"""
        curr = self.curr()
        if curr is None:
            return None

        self.idx += 1  # assume success and consume keyword
        match curr.ty:
            case TokenType.Define:
                return self.define()
            case TokenType.If:
                return self.if_expr()
            case TokenType.Cond:
                return self.cond()
            case TokenType.Begin:
                return self.begin()
            case TokenType.Lambda:
                return self.lambda_expr()
            case TokenType.Let:
                return self.let()

        self.idx -= 1  # no keyword, go back

        return None

    def application(self) -> ast.AST:
        self.consume(TokenType.LParen)

        specials = self.specials()
        if specials is not None:
            self.consume(TokenType.RParen)
            return specials

        fun = self.expression()

        args: List[ast.AST] = []
        while not self.check(TokenType.RParen):
            args.append(self.expression())

        self.consume(TokenType.RParen)

        return ast.Application(fun, args)

    def expression(self) -> ast.AST:
        """Parse a single expression"""

        curr = self.curr()
        if curr is None:
            self.raiseSyntaxError("Expecting expression found EOF")

        match curr.ty:
            case TokenType.LParen:
                # peek to check if its followed by RParen
                self.idx += 1
                if self.check(TokenType.RParen):
                    self.idx += 1
                    return ast.Nil()

                self.idx -= 1  # unpeek

                return self.application()

            case TokenType.ID:
                self.idx += 1
                return ast.Identifier(curr)
            case TokenType.Nil:
                self.idx += 1
                return ast.Nil()
            case TokenType.Truth | TokenType.Falsity:
                self.idx += 1
                return ast.BooleanLiteral(curr)
            case TokenType.Integer:
                self.idx += 1
                return ast.IntLiteral(curr)
            case TokenType.Float:
                self.idx += 1
                return ast.FloatLiteral(curr)
            case TokenType.String:
                self.idx += 1
                return ast.StringLiteral(curr)

        self.raiseSyntaxError("Expecting expression")

    def expression_list(self) -> List[ast.AST]:
        asts: List[ast.AST] = []

        # take EOF to account
        while self.idx < len(self.tokens) - 1 and \
                not self.check(TokenType.RParen):
            asts.append(self.expression())

        return asts

    def parse(self, tokens: List[Token]) -> ast.Program:
        """Parse tokens that collects list of expressions into Program"""
        self.idx = 0
        self.tokens = tokens
        return ast.Program(self.expression_list())
